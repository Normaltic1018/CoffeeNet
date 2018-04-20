import glob, sys
import importlib
from coffee_lib.interface import coffee_util as util
from coffee_lib.interface import message

class Consultant:

    def __init__(self, options):
        self.loaded_tools = {}
        self.load_tools(options)
        self.mainmenu_commands = {
                "list": "List available tools",
                "use": "Use a specific tool",
                "info": "Information on a specific tool",
                "update": "Update CoffeeNet",
                "exit": "Exit CoffeeNet"}
        self.number_of_tools = len(self.loaded_tools)
        self.cl_option = options

    def load_tools(self, options):
        for name in glob.glob('Tools/*/tool.py'):
            if name.endswith(".py") and ("__init__" not in name):
                tool_module = importlib.import_module(name.replace("/", ".").rstrip(".py"))
                self.loaded_tools[name] = tool_module.Tools(options)
                
        return

    def list_tools(self):
        message.title()
        
        index_tools = 1
        print(util.color(' [#] Available Tools: \n'))
        for key, tool in sorted(self.loaded_tools.items()):
            print('\t' + str(index_tools) + ")\t" + tool.tool_name)
            index_tools += 1
        
        print("\nCoffee > Did you Check it?")
        print("Coffee > " +util.color("[ Press Enter to go back to the menu ]", bold=True))
        print()

        return

                
    def main_menu(self):
        user_command = ""
        menu_show = True

        try:
            while user_command == "":
                
                if menu_show:
                    message.title()
                    print(util.color("Coffee :", warning=True)+"\t" + util.color(str(self.number_of_tools)) + " tools loaded\n")
                    print("Availabe Commands:\n")
                    for command in list(self.mainmenu_commands.keys()):
                        print("\t" + util.color(command) + "\t\t\t" + self.mainmenu_commands[command])
                    print()

                user_command = input("Coffee < ").strip()
                
                if user_command.startswith('list'):
                    self.list_tools()
                    menu_show = False
                    user_command = ''
                
                elif user_command.startswith('use'):
                    #check user command ( use [number or tool name] )
                    if len(user_command.split()) == 1:
                        # Not enought Param
                        self.list_tools()
                        menu_show = False
                        

                    elif len(user_command.split()) == 2:
                        tool_select = user_command.split()[1]

                        # check it is number
                        if tool_select.isdigit() and 0 < int(tool_select) <= self.number_of_tools:
                            tool_index = 1
                            for key, tool_obj in sorted(self.loaded_tools.items()):
                                if int(tool_select) == tool_index:
                                    tool_obj.main_menu()
                                    tool_index += 1
                                    main_show = True
                                else:
                                    tool_index += 1
                            menu_show = True
                            

                        # check it is tool name
                        else:
                            for key, tool_obj in sorted(self.loaded_tools.items()):
                                if tool_select.lower() == tool_obj.tool_name.lower():
                                    tool_obj.main_menu()
                                    menu_show = True
                    else:
                        pass

                    user_command = ''

                elif user_command.startswith('info'):
                    if len(user_command.split()) == 1:
                        menu_show = False
                        message.info()
                        user_command = ''

                    elif len(user_command.split()) == 2:
                        info_select = user_command.split()[1]

                        if info_select.isdigit() and 0<int(info_select) <= self.number_of_tools:
                            tool_index = 1
                            for key, tool_obj in sorted(self.loaded_tools.items()):
                                if int(info_select) == tool_index:
                                    print()
                                    print(util.color(tool_obj.tool_name) + tool_obj.description)
                                    print()
                                    menu_show = False
                                tool_index += 1

                        # in case, tool name input
                        else:
                            for key, tool_obj in sorted(self.loaded_tools.items()):
                                if info_select.lower() == tool_obj.tool_name.lower():
                                    print()
                                    print(util.color(tool_obj.tool_name) + tool_obj.description)
                                    print()
                                    menu_show = False
                        user_command = ''
                    else:
                        user_command = ''
                        menu_show = True

                elif user_command.startswith('exit'):        
                    print("\n\n" + util.color("Exit CoffeeNet... Have a Good Day!", warning=True))
                    sys.exit()
                elif user_command.startswith('update'):
                    user_command = ''
                    menu_show = False
                    print("Coffee > Sorry, \"Update\" Command is not supported in 1.0 Version.")

                else:
                    menu_show = True
                    user_command = ''


        except KeyboardInterrupt:
            print("\n\n" + util.color("Exit CoffeeNet... Have a Good Day!", warning=True))
            sys.exit()



