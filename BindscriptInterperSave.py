#Sample print: print::Hello;
#Sample print+modifier_url: print::[url] https://example.com;
#If statement: if something = thing | call function

import re
import requests

mods = {
        "url":"URL_MOD",
        "reg":"FUNCTION_REGISTRY_MOD",
        "arith":"ARITHMATIC_MOD",
        "bool":"BOOL_MOD",
        "rev":"REVERSE_MOD",

        #Backwards usage
        "URL_MOD":"url",
        "FUNCTION_REGISTRY_MOD":"url",
        "ARITHMATIC_MOD":"arith",
        "BOOL_MOD":"bool",
        "REVERSE_MOD":"rev"

    }
debug = False
regged_funcs = []
state = "" 
user_var = ""
current_variable = ""

def bs_ConvertList(list_):
    intr = ""
    if isinstance(list_, list):
        current = 0
        all_ = len(list_)
        while (current != all_):
            intr += list_[current] + ","
            current += 1
        intr[len(intr)] = ""
        return intr
def DumpData(data):
    s = f'''
[DUMPSTART]
{data}
[DUMPEND]

    '''
    open('crashdump.bcd','a').write(s)

#TODO: Finish modifiers

def bs_ReadModifier(par_with_mod):

    def a_m(o):
        return "[" + o + "]"

    if (par_with_mod[0] == "[") and (par_with_mod.split("]")[0].replace("[","") in mods):
        if (StartsWith(par_with_mod,mods["URL_MOD"]):
            return requests.get(par_with_mod,'html.parser').text()
        elif (StartsWith(par_with_mod, mode["FUNCTION_REGISTRY_MOD"])):
            return bs_ConvertList(regged_funcs)
            


def bs_LogMsg(msg):
    if (debug == True):
        open('execlog.log','a').write(f'\n[BINDSCRIPT_BETA] {msg}')

def StartsWith(obj, startswith):
    if (obj[0:len(startswith)] == startswith):
        return True
    else:
        return False

def EndsWith(obj, endwith):
    if (obj[len(obj)-len(endwith):len(obj)] == endwith):
        return True
    else:
        return False



def bs_RegisterFunction(FunctionName, FunctionCode):
    
    regged_funcs.append(f'{FunctionName}~{FunctionCode}')

def bs_ReadFunc(funccall):
    global regged_funcs
    function_type = funccall.split("::")[0]
    
    __all__ = len(regged_funcs)
    __current__ = 0

    while (__all__ != __current__):
        bs_LogMsg("STARTED LOOP!")
        if (regged_funcs[__current__].split("~")[0] == function_type):
            bs_LogMsg('COMFIRMED FUNCTION TYPE')
            try:
                eval(regged_funcs[__current__].split("~")[1].replace('__BS_USER_VAR__', '"' + funccall.split('::')[1].replace(';','') + '"' ))
                bs_LogMsg("EXECUTED FUNCTION")
            except Exception as inst:

                dump_msg = f'''
                {type(inst)}
                Got An Exception While Calling Function |[{function_type}]| 
                '''
                bs_LogMsg("GOT AN EXCEPTION!")

                bs_LogMsg(type(inst))
                print(inst)
                print(f'Got an exception while calling function "{function_type}" (Syntax Error?)')
                DumpData(re.sub(r"[\n\t\s]*","",dump_msg))

        #elif (StartsWith(funccall,'if')):
            #if (funccall.split('|')[0].replace('if',''))
        __current__ += 1

def bs_ReadDoc(doc_filename):
    current = 0
    all_ = str(open(doc_filename, 'r').read()).split('\n')
    all_str = len(all_)

    while (current != all_str):
        bs_ReadFunc(all_[current])
        current += 1
    

#Functions
bs_RegisterFunction("print","print(__BS_USER_VAR__)")      
bs_RegisterFunction("newfile","open(__BS_USER_VAR__,'x')")
bs_RegisterFunction("writefile","open(__BS_USER_VAR__.split(',')[0],__BS_USER_VAR__.split(',')[1]")
bs_RegisterFunction('env_add', 'import __BS_USER_VAR__')
bs_RegisterFunction("readfile","print(open(__BS_USER_VAR__,'r').read())")
bs_RegisterFunction("getreg",f"print('{bs_ConvertList(regged_funcs)}')")
bs_ReadDoc('testfile.bs')
print(mods["URL_MOD"])
