from coffee_lib.interface import coffee_util as util
import os

version = "1.0"

def title():
    title_data =  " " + "="*82 + "\n"
    title_data += "| " + "  ______            ______   ______                  __    __            __     " + " |\n"
    title_data += "| " + " /      \          /      \ /      \                /  \  /  |          /  |    " + " |\n"
    title_data += "| " + "/$$$$$$  | ______ /$$$$$$  /$$$$$$  ______   ______ $$  \ $$ | ______  _$$ |_   " + " |\n"
    title_data += "| " + "$$ |  $$/ /      \$$ |_ $$/$$ |_ $$/      \ /      \$$$  \$$ |/      \/ $$   |  " + " |\n"
    title_data += "| " + "$$ |     /$$$$$$  $$   |   $$   | /$$$$$$  /$$$$$$  $$$$  $$ /$$$$$$  $$$$$$/   " + " |\n"
    title_data += "| " + "$$ |   __$$ |  $$ $$$$/    $$$$/  $$    $$ $$    $$ $$ $$ $$ $$    $$ | $$ | __ " + " |\n"
    title_data += "| " + "$$ \__/  $$ \__$$ $$ |     $$ |   $$$$$$$$/$$$$$$$$/$$ |$$$$ $$$$$$$$/  $$ |/  |" + " |\n"
    title_data += "| " + "$$    $$/$$    $$/$$ |     $$ |   $$       $$       $$ | $$$ $$       | $$  $$/ " + " |\n"
    title_data += "| " + " $$$$$$/  $$$$$$/ $$/      $$/     $$$$$$$/ $$$$$$$/$$/   $$/ $$$$$$$/   $$$$/  " + " |\n"
    title_data += "|" + " "*82 + "|\n"
    title_data += "|" + " "*82 + "|\n"
    title_data += "|" + " "*65 + "CoffeeNet v"+ version + " "*3 + "|\n"
    title_data += " " + "="*82 + "\n"
    title_data += "|" + " made by Normaltic"+" "*30 +"[E-mail]: rlagkstn1426@naver.com  " + "|\n"
    title_data += " " + "="*82 + "\n"
    
    os.system("clear")
    print(title_data)
    return

def info():
    info_data =  " " + "="*59 + "\n"
    info_data += "|" + " Hi, I am normaltic." + " "*39 +"|\n"
    info_data += "|" + " CoffeeNet is for Small Network like cafe, library, etc    " + "|\n"
    info_data += "|" + " "*59 +"|\n"
    info_data += "|" + " Scan your Network using scanner tool in CoffeeNet " +" "*8 + "|\n"
    info_data += "|" + " And If you want, YOU CAN create sniffing ENV " + " "*13 +"|\n"
    info_data += "|" + " Enjoy your HACK LIFE " + " "*37 + "|\n"
    info_data += " " + "="*59 + "\n"
    info_data += "\n"+util.color("USAGE") + "\n"
    info_data += " Command[info]\t->\tinfo [Number or tool_name]\n"
    info_data += " Command[use]\t->\tuse [Number or Tool Name] \n"
    print(info_data)
    return

def tool_title(name, version):
    scanner_title = "="*80 + "\n"
    scanner_title += " "*30 + util.color("CoffeeNet " + name, bold=True) +"\n"
    scanner_title += " " * 60 + "Version : " + version +"\n"
    scanner_title += "="*80 + "\n"
    os.system("clear")
    print(scanner_title)

