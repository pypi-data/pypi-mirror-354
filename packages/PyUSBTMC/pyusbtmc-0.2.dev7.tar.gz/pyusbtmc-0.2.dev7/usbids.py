#!python
"""
names.c/names.h from linux-usb source code
on Ubuntu linux you can find usb.ids at /usr/share/misc/usb.ids
man page of lsusb says:/var/lib/usbutils/usb.ids
/usr/share/misc/usb.ids is a link to this file.
"""
import os.path, sys
import logging

class vendors_t(dict):
    def __init__(self,*args,**env):
        dict.__init__(self,*args,**env)
    def add(self, vendorid, name):
        self[vendorid]=name

class products_t(dict):
    def __init__(self,*args,**env):
        dict.__init__(self,*args,**env)
    def add(self, vendorid,productid, name):
        self[(vendorid,productid)]=name

class usb_classes_t(dict):
    def __init__(self,*args,**env):
        dict.__init__(self,*args,**env)
    def add(self, classid, name):
        self[classid]=name

class usb_subclasses_t(dict):
    def __init__(self,*args,**env):
        dict.__init__(self,*args,**env)
    def add(self, classid, subclassid,name):
        self[(classid,subclassid)]=name

class protocols_t(dict):
    def __init__(self,*args,**env):
        dict.__init__(self,*args,**env)
    def add(self, classid,subclassid,protocoid, name):
        self[(classid,subclassid,protocoid)]=name

class audioterminals_t(dict):
    def __init__(self,*args,**env):
        dict.__init__(self,*args,**env)
    def add(self, termt,name):
        self[termt]=name

class videoterminals_t(dict):
    def __init__(self,*args,**env):
        dict.__init__(self,*args,**env)
    def add(self, termt, name):
        self[termt]=name

class hashtbl_t(dict):
    def __init__(self,*args,**env):
        dict.__init__(self,*args,**env)
    def add(self, key, name):
        self[key]=name

vendors=vendors_t()
products=products_t()

usb_classes=usb_classes_t()
usb_subclasses=usb_subclasses_t()
protocols=protocols_t()

import re
# comments
comment_pattern=re.compile(r"^\s*#.+$|^\s*$")
# Vendors, devices and interfaces. Please keep sorted.
vendor_pattern=re.compile(r"^(?P<id>[0-9A-Fa-f]+)\s+(?P<name>.+)")
product_pattern=re.compile(r"^\t(?P<id>[0-9A-Fa-f]+)\s+(?P<name>.+)")
interface_pattern=re.compile(r"^\t\t(?P<id>[0-9A-Fa-f]+)\s+(?P<name>.+)")

# List of known device classes, subclasses and protocols
class_pattern=re.compile(r"^C\s+(?P<id>[0-9A-Fa-f]+)\s+(?P<name>.+)")
subclass_pattern=re.compile(r"^\t(?P<id>[0-9A-Fa-f]+)\s+(?P<name>.+)")
protocol_pattern=re.compile(r"^\t\t(?P<id>[0-9A-Fa-f]+)\s+(?P<name>.+)")

#audio terminal
at_pattern=re.compile(r"^AT\s+(?P<id>[0-9A-Fa-f]+)\s+(?P<name>.+)")
audioterminals=audioterminals_t()

#
hid_pattern=re.compile(r"^HID\s+(?P<id>[0-9A-Fa-f]+)\s+(?P<name>.+)")
hiddescriptors=hashtbl_t()

#HID Descriptor Item types
R_pattern=re.compile(r"^R\s+(?P<id>[0-9A-Fa-f]+)\s+(?P<name>.+)")
reports=hashtbl_t()

# List of Physical Descriptor Bias Types
BIAS_pattern=re.compile(r"^BIAS\s+(?P<id>[0-9A-Fa-f]+)\s+(?P<name>.+)")
biass=hashtbl_t()

# List of Physical Descriptor Item Types
PHY_pattern=re.compile(r"^PHY\s+(?P<id>[0-9A-Fa-f]+)\s+(?P<name>.+)")
physdess=hashtbl_t()

# List of HID Usages
HUT_pattern=re.compile(r"^HUT\s+(?P<id>[0-9A-Fa-f]+)\s+(?P<name>.+)")
hid_usage_pattern=re.compile(r"^\t(?P<id>[0-9A-Fa-f]+)\s+(?P<name>.+)")
huts=hashtbl_t()
hutus=hashtbl_t()

# List of Languages
LANGID_pattern=re.compile(r"^L\s+(?P<id>[0-9A-Fa-f]+)\s+(?P<name>.+)")
dialect_pattern=re.compile(r"^\t(?P<id>[0-9A-Fa-f]+)\s+(?P<name>.+)")
langids=hashtbl_t()
dialects=hashtbl_t()

# HID Descriptor bCountryCode
HCC_pattern=re.compile(r"^HCC\s+(?P<id>[0-9A-Fa-f]+)\s+(?P<name>.+)")
countrycodes=hashtbl_t()
# List of Video Class Terminal Types
VT_pattern=re.compile(r"^VT\s+(?P<id>[0-9A-Fa-f]+)\s+(?P<name>.+)")
videoterminals=videoterminals_t()

class usbids_file(object):
    pass

def parse(f:usbids_file):# f:usbids_file object
    try:
        l=f.next()
        while(l):
            if (comment_pattern.match(l)):
                l=f.next()
                continue
            elif(VT_pattern.match(l)):
                d=VT_pattern.match(l).groupdict()
                vtid=int(d["id"],16)
                videoterminals.add(vtid,d["name"])
                l=f.next()
                continue
            elif(HCC_pattern.match(l)):
                d=HCC_pattern.match(l).groupdict()
                ccid=int(d["id"],16)
                countrycodes.add(ccid,d["name"])
                l=f.next()
                continue
            elif(PHY_pattern.match(l)):
                d=PHY_pattern.match(l).groupdict()
                phyid=int(d["id"],16)
                physdess.add(phyid,d["name"])
                l=f.next()
                continue
            elif(BIAS_pattern.match(l)):
                d=BIAS_pattern.match(l).groupdict()
                biasid=int(d["id"],16)
                biass.add(biasid,d["name"])
                l=f.next()
                continue
            elif(R_pattern.match(l)):
                d=R_pattern.match(l).groupdict()
                rid=int(d["id"],16)
                reports.add(rid,d["name"])
                l=f.next()
                continue
            elif(hid_pattern.match(l)):
                d=hid_pattern.match(l).groupdict()
                hidid=int(d["id"],16)
                hiddescriptors.add(hidid,d["name"])
                l=f.next()
                continue
            elif(at_pattern.match(l)):
                d=at_pattern.match(l).groupdict()
                atid=int(d["id"],16)
                audioterminals.add(atid,d["name"])
                l=f.next()
                continue
            elif(LANGID_pattern.match(l)):
                d=LANGID_pattern.match(l).groupdict()
                langid=int(d["id"],16)
                langids.add(langid,d["name"])
                l=f.next()
                while(l):
                    if (comment_pattern.match(l)):
                        l=f.next()
                        continue
                    elif(dialect_pattern.match(l)):
                        d=dialect_pattern.match(l).groupdict()
                        dialectid=int(d["id"],16)
                        dialects.add((langid,dialectid),d["name"])
                        l=f.next()
                        continue
                    else:
                        break
                continue
            elif(HUT_pattern.match(l)):
                d=HUT_pattern.match(l).groupdict()
                hutid=int(d["id"],16)
                huts.add(hutid,d["name"])
                l=f.next()
                while(l):
                    if (comment_pattern.match(l)):
                        l=f.next()
                        continue
                    elif(hid_usage_pattern.match(l)):
                        d=hid_usage_pattern.match(l).groupdict()
                        hutuid=int(d["id"],16)
                        hutus.add((hutid,hutuid),d["name"])
                        l=f.next()
                        continue
                    else:
                        break
                continue
            elif(class_pattern.match(l)):
                d=class_pattern.match(l).groupdict()
                classid=int(d["id"],16)
                usb_classes.add(classid,d["name"])
                l=f.next()
                while(l):
                    if (comment_pattern.match(l)):
                        l=f.next()
                        continue
                    elif(subclass_pattern.match(l)):
                        d=subclass_pattern.match(l).groupdict()
                        subclassid=int(d["id"],16)
                        usb_subclasses.add(classid, subclassid, d["name"])
                        l=f.next()
                        while(l):
                            if (comment_pattern.match(l)):
                                l=f.next()
                                continue
                            elif(protocol_pattern.match(l)):
                                d=protocol_pattern.match(l).groupdict()
                                protocolid=int(d["id"],16)
                                protocols.add(classid, subclassid,protocolid, d["name"])
                                l=f.next()
                                continue
                            else:
                                break
                        continue
                    else:
                        break
                continue
            elif (vendor_pattern.match(l)):
                d=vendor_pattern.match(l).groupdict()
                vendorid=int(d["id"],16)
                vendors.add(vendorid,d["name"])
                l=f.next()
                while(l):
                    if (comment_pattern.match(l)):
                        l=f.next()
                        continue
                    elif(product_pattern.match(l)):
                        d=product_pattern.match(l).groupdict()
                        deviceid=int(d["id"],16)
                        products.add(vendorid,deviceid,d["name"])
                        l=f.next()
                        continue
                    else:
                        break
                continue
            else:
                l=f.next()
    except StopIteration:
        pass
# distributed usb.ids encoded in latin_1 or iso8859_15 or cp1252(winodws-1252). it is not ascii nor utf-8

# python2.6 does not have version_info
# sys.version_info is vesion_info type in python2.7/3

class usbids_file(object):
    def __init__(self,fname="./usb.ids"):
        if sys.version_info >= (3,):
            self.next=self.next3
        else:
            self.next=self.next2
        if fname:
            self.load_file(fname)
            
    def load_file(self,fname="./usb.ids"):
        if sys.version_info  >= (3,) :
            self.fd=open(fname,encoding="latin1")
        else:
            self.fd=open(fname)
        
    def next3(self):# next for Python3
        s=self.fd.readline()
        if type(s) == bytes:
            return s.decode('latin1')
        else: # str/unicode
            return s
        
    def next2(self):# next fo Python2
        s=self.fd.readline()
        if type(s) == str: # bytes/str
            return s.decode('latin1')
        else: # unicode
            return s

    @classmethod
    def update_file_from_web(
            cls,
            source_url="http://www.linux-usb.org/usb.ids",
            dest_fname="./usb.ids"
    ):
        if sys.version_info >= (3,):
            from  urllib.request import urlopen
        else:
            from  urllib import urlopen
        s=urlopen(source_url)
        with open(dest_fname, "wb") as f:
            for l in s:
                f.write(l)

    def open_web(self,
                 source_url="http://www.linux-usb.org/usb.ids",
                 dest_fname="usb.ids"
    ):
        if sys.version_info >  (3,) :
            from  urllib.request import urlopen
            from io import StringIO
        else:
            from  urllib import urlopen
            from cStringIO import StringIO
        s=urlopen(source_url)
        self.fd=s
    
    @classmethod
    def find_usbids(cls):
        f=None
        for d in [
                ".",
                "/usr/share/misc", "/var/lib/usbutils",
                "/usr/share/hwdata",
                os.path.join(sys.prefix,"share/misc"),
                "share/misc",
        ]+[
            os.path.join(d, "../share/misc") for d in sys.path
        ]+["."] :
            f=os.path.join(d,"usb.ids")
            if os.path.isfile(f):
                return f
            else:
                continue
        # for d in sys.path:
        #     f=os.path.join(d, "../share/misc", "usb.ids")
        #     if os.path.isfile(f):
        #         return f
        #     else:
        #         continue
        raise RuntimeError("no usb.ids file found")

__initialized = False

def init_usbids():
    if __initialized:
        return
    uf=usbids_file("")
    try:
        fn = uf.find_usbids()
    except RuntimeError as erm:
        logging.warn(erm)
        uf.open_web()
    else:
        uf.load_file(fn)
    parse(uf)

if not __initialized:
    init_usbids()
    __initialized = True
