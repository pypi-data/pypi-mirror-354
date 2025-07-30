#!/usr/bin/env python
import requests
from zebra import Zebra
import qrcode
from math import ceil, floor
from PIL import Image
import textwrap
import argparse
import sys

# make substitutions for characters not in CP437

def subst(s):
    repl={}
    repl["®"]="(R)"
    repl["©"]="(C)"
    repl["Ω"]="Ω" # U+2126 -> U+03A9, which is in CP437
    repl["±"]="+/-"
    out=""
    for i in s:
        try:
            out=out+repl[i]
        except:
            out=out+i
    return out

# filter out characters not in selected codepage
# (printer uses CP437)

def filter(s, cp):
    out=""
    for i in s:
        try:
            i.encode(cp)
            out=out+i
        except:
            pass
    return out

# handle escape characters in strings to be printed

def esc(s):
    out=""
    for i in s:
        if i=="\"":
            out=out+"\\\""
        elif i=="\\":
            out=out+"\\\\"
        else:
            out=out+i
    return out

# render a line of text at coordinates
# return coordinates of next line

def textline(z, res, s, loc, fontnum):
    z.output(f"A{loc[0]},{loc[1]},0,{fontnum},1,1,N,\"{esc(filter(subst(s), "cp437"))}\"\n")
    return (loc[0], loc[1]+font_metrics(res)[fontnum][1])

# wrap text in a bounding box at coordinates
# return coordinates of next line and any unused text

def textbox(z, res, s, loc, bbox, fontnum):
    wrapped=textwrap.wrap(filter(subst(s), "cp437"), width=floor(bbox[0]/font_metrics(res)[fontnum][0]))
    line=0
    while line*font_metrics(res)[fontnum][1]<bbox[1] and line<len(wrapped):
        loc=textline(z, res, wrapped[line], loc, fontnum)
        line=line+1
    return loc, " ".join(wrapped[line:])

# render a QR code at coordinates
# return size (single value, since QR codes are square)

def qr(z, s, loc, mul, brdr):
    qr = qrcode.QRCode(
        box_size=mul,
        border=brdr,
    )
    qr.add_data(s)
    qr.make(fit=True)
    img = qr.make_image().copy()
    padded=Image.new(mode="1", size=(8*ceil(img.width/8),img.height), color="white")
    padded.paste(im=img, box=(0,0,img.width,img.height))
    z.output(f"GW10,10,{ceil(padded.width/8)},{padded.height},{padded.tobytes().decode("cp437")}\n")
    return img.height

    # width and height for built-in monospace fonts (includes whitespace)

def font_metrics(res):
    m={}
    if res==203:
        m[1]=(10,14)
        m[2]=(12,18)
        m[3]=(14,22)
        m[4]=(16,26)
        m[5]=(34,50)
    if res==300:
        m[1]=(14,22)
        m[2]=(18,30)
        m[3]=(22,38)
        m[4]=(26,46)
        m[5]=(50,82)
    return m

# entrypoint

def cli():
    parser=argparse.ArgumentParser()
    parser.add_argument("id", help="part ID (or IPN)")
    parser.add_argument("-i", action="store_true", help="search by IPN instead of part ID")
    parser.add_argument("-x", help="label width, in inches (default: 2\")", type=float)
    parser.add_argument("-y", help="label height, in inches (default: 1\")", type=float)
    parser.add_argument("-g", help="label gap, in inches (default: 0.118\")", type=float)
    parser.add_argument("-q", help="send to selected print queue instead of stdout")
    parser.add_argument("-p", help="PartDB base URL")
    parser.add_argument("-k", help="PartDB API key")
    parser.add_argument("-r", help="printer resolution (default: 203 dpi)", type=int)
    parser.add_argument('-v', action='version', version='%(prog)s 0.3.1')
    args=parser.parse_args()
    id=args.id
    if args.x==None:
        label_width=2
    else:
        label_width=args.x
    if args.y==None:
        label_height=1
    else:
        label_height=args.y
    if args.g==None:
        label_gap=0.118
    else:
        label_gap=args.g
    if args.q==None:
        queue="zebra_python_unittest"
    else:
        queue=args.q
    base_url=args.p
    api_key=args.k
    if args.r==None:
        res=203
    else:
        res=args.r
        if res!=203 and res!=300:
            raise ValueError("valid resolution options are 203 and 300")

    # look up the part

    if args.i==True:
        url=f"{base_url}/api/parts/?ipn={id}"
    else:
        url=f"{base_url}/api/parts/{id}"
    headers={}
    headers["Accept"]="application/json"
    if api_key!=None:
        headers["Authorization"]=f"Bearer {api_key}"
    part=requests.get(url, headers=headers).json()
    if args.i==True: # search by IPN
        try:
            part=part[0] 
        except IndexError:
            sys.exit("part not found")
    try:
        if part["status"]==404: # catch a search that returns nothing
            sys.exit("part not found")
    except KeyError:
        pass

    # render a label for it

    label_width=floor(label_width*res)
    label_height=floor(label_height*res)
    label_gap=floor(label_gap*res)

    z=Zebra(queue)
    z.output(f"q{label_width}\n") 
    if (args.y!=None and args.g!=None):
        z.output(f"Q{label_height},{label_gap}\n")
    z.output("N\n")

    if res==300:
        qr_size=qr(z, f"{base_url}/en/part/{id}", (10, 10), 6, 3)
    else:
        qr_size=qr(z, f"{base_url}/en/part/{id}", (10, 10), 4, 2)

    loc=(15+qr_size, 20)
    try:
        loc=textline(z, res, part["ipn"], loc, 5)
    except KeyError:
        loc=textline(z, res, "", loc, 5)

    try:
        loc, excess=textbox(z, res, f"{part["manufacturer"]["name"]} {part["manufacturer_product_number"]}", loc, (label_width-loc[0]-10, label_height-loc[1]-10), 2)
    except KeyError:
        loc, excess=textbox(z, res, "", loc, (label_width-loc[0]-10, label_height-loc[1]-10), 2)

    avail_y=floor((20+qr_size-loc[1])/font_metrics(res)[2][1])*font_metrics(res)[2][1]
    loc, excess=textbox(z, res, part["description"], loc, (label_width-loc[0]-10, avail_y), 2)
    if excess!="":
        loc=(10, loc[1])
        loc, excess=textbox(z, res, excess, loc, (label_width-20, label_height-loc[1]), 2)

    z.output("P1\n")

if __name__ == "__main__":
    cli()
