import json, os, datetime

COMMANDS = ["add", "subtract", "push", "overview", "help", "percentages", "reset"]

class App:
    def __init__(self):
        self.date = datetime.date.today()
        self.week = self.date.isocalendar().week
        self.data = {
            "week" : 0,
            "income" : 0.0,
            "balanceNeeds" : 0.0,
            "balanceWants" : 0.0,
            "balanceSavings" : 0.0,
            "nextNeeds" : 0.0,
            "nextWants" : 0.0,
            "nextSavings" : 0.0,
            "totalExpenses" : 0.0,
            "totalIncome" : 0.0,
            "percentNeeds" : 0.5,
            "percentWants" : 0.3,
            "percentSavings" : 0.2
        }
        
        # Load data from file
        self._load()
        
    def _printBalances(self):
        self._calculateBalances()
        print(f'--This Week--\nTotal: {self.data["income"]}\nNeeds: {self.data["balanceNeeds"]}\nWants: {self.data["balanceWants"]}\nSavings: {self.data["balanceSavings"]}\n\n--Next Week--\nTotal: {self.data["income"]}\nNeeds: {self.data["nextNeeds"]}\nWants: {self.data["nextWants"]}\nSavings: {self.data["nextSavings"]}')
        
    def _readCommand(self, commandString:str):
        command = commandString.split()
        if command[0].lower() not in COMMANDS:
            raise KeyError("Invalid command")
        
        match command[0]:
            case ("help"):
                self.help()
            case ("overview"):
                self.overview()
            case ("reset"):
                self.reset()
            case ("add"):
                self.add(command[1], command[2])
            case ("subtract"):
                self.subtract(command[1], command[2])
            case ("push"):
                self.push(command[1], command[2])
            case ("pull"):
                self.pull(command[1], command[2])
            case ("percentages"):
                self.percentages(command[1], command[2], command[3])
            case _:
                raise KeyError("Invalid command")
        
    def _calculateBalances(self):
        self.data["balanceNeeds"]   = self.data["income"] * self.data["percentNeeds"]
        self.data["balanceWants"]   = self.data["income"] * self.data["percentWants"]
        self.data["balanceSavings"] = self.data["income"] * self.data["percentSavings"]
        
    def _addExpense(self, amount):
        self.data["totalExpenses"] += amount
        self._save()
    
    def _addIncome(self, amount):
        self.data["totalIncome"] += amount
        self.data["income"] += amount
        self._save()
    
    def _subtractExpense(self, amount):
        if amount > self.data["totalExpenses"]:
            self.data["totalExpenses"] = 0.0
        else:
            self.data["totalExpenses"] -= amount
        self._save()
    
    def _subtractIncome(self, amount):
        if amount > self.data["totalIncome"]:
            self.data["totalIncome"] = 0.0
        else:
            self.data["totalIncome"] -= amount
            self.data["income"] -= amount
        self._save()
        
    def _pushNeeds(self, amount):
        if amount > self.data["balanceNeeds"]:
            amount = self.data["balanceNeeds"]
        elif amount < 0:
            amount = 0
            
        self.data["balanceNeeds"] -= amount
        self.data["nextNeeds"] += amount
    
    def _pushWants(self, amount):
        if amount > self.data["balanceWants"]:
            amount = self.data["balanceWants"]
        elif amount < 0:
            amount = 0
            
        self.data["balanceWants"] -= amount
        self.data["nextWants"] += amount
    
    def _pushSavings(self, amount):
        if amount > self.data["balanceSavings"]:
            amount = self.data["balanceSavings"]
        elif amount < 0:
            amount = 0
            
        self.data["balanceSavings"] -= amount
        self.data["nextSavings"] += amount
            
    def _pullNeeds(self, amount):
        if amount > self.data["nextNeeds"]:
            amount = self.data["nextNeeds"]
        elif amount < 0:
            amount = 0
            
        self.data["balanceSavings"] += amount
        self.data["nextSavings"] -= amount
    
    def _pullWants(self, amount):
        if amount > self.data["nextWants"]:
            amount = self.data["nextWants"]
        elif amount < 0:
            amount = 0
            
        self.data["balanceSavings"] += amount
        self.data["nextSavings"] -= amount
    
    def _pullSavings(self, amount):
        if amount > self.data["nextSavings"]:
            amount = self.data["nextSavings"]
        elif amount < 0:
            amount = 0
            
        self.data["balanceSavings"] += amount
        self.data["nextSavings"] -= amount
        
    def _save(self):
        _dataString = json.dumps(self.data)
        file = open("user_data/data.json", "w")
        file.write(_dataString)
        
    def _load(self):
        if not os.path.exists("user_data/data.json"):
            open("user_data/data.json", "w").close()
        file = open("user_data/data.json", "r")
        try:
            self.data = json.loads(file.read())
        except json.decoder.JSONDecodeError:
            pass
        
    ## Commands
    def help(self):
        '''Shows a list of commands and their arguments'''
        print("--COMMANDS--\nhelp\noverview\nadd ['income'/'expense'] [amount]\nsubtract ['income'/'expense'] [amount]\npush ['needs'/'wants'/'savings'] [amount]\npercentages [needs%] [wants%] [savings%]reset")
    
    def overview(self):
        '''Prints an overview of the current totals and balances'''
        self._calculateBalances()
        print(f'--This Week--\nTotal: {self.data["income"]}\nNeeds: {self.data["balanceNeeds"]}\nWants: {self.data["balanceWants"]}\nSavings: {self.data["balanceSavings"]}\n\n--Next Week--\n')
    
    def add(self, group:str, amount):
        '''Adds an amount to a group'''
        # Check amount
        try:
            amount = float(amount)
        except ValueError:
            return print("ERROR: argument 'amount' must be a float.")
        
        # Check group
        if (group.lower() == "income"):
            self._addIncome(amount)
        elif (group.lower() == "expense"):
            self._addExpense(amount)
        else:
            return print("ERROR: Unknown group. Please use either 'income' or 'expense'.")
        
    def subtract(self, group:str, amount):
        '''Subtracts an amount from a group'''
        # Check amount
        try:
            amount = float(amount)
        except ValueError:
            return print("ERROR: argument 'amount' must be a float.")
        
        # Check group
        if (group.lower() == "income"):
            self._subtractIncome(amount)
        elif (group.lower() == "expense"):
            self._subtractExpense(amount)
        else:
            return print("ERROR: Unknown group. Please use either 'income' or 'expense'.")
        
    def push(self, group:str, amount):
        '''Pushes an amount to a certain group'''
        # Check amount
        try:
            amount = float(amount)
        except ValueError:
            return print("ERROR: argument 'amount' must be a float.")
        
        # Check group
        if (group.lower() == "needs"):
            self._pushNeeds(amount)
        elif (group.lower() == "wants"):
            self._pushWants(amount)
        elif (group.lower() == "savings"):
            self._pushSavings(amount)
        else:
            return print("ERROR: Unknown group. Please use either 'needs', 'wants', or 'savings'.")
        
    def pull(self, group:str, amount):
        '''Pulls an amount from a certain group'''
        # Check amount
        try:
            amount = float(amount)
        except ValueError:
            return print("ERROR: argument 'amount' must be a float.")
        
        # Check group
        if (group.lower() == "needs"):
            self._pullNeeds(amount)
        elif (group.lower() == "wants"):
            self._pullWants(amount)
        elif (group.lower() == "savings"):
            self._pullSavings(amount)
        else:
            return print("ERROR: Unknown group. Please use either 'needs', 'wants', or 'savings'.")
        
    def percentages(self, needs, wants, savings):
        try:
            needs = float(needs)/100
            wants = float(wants)/100
            savings = float(savings)/100
        except ValueError:
            return print("ERROR: arguments must be floats")
        
        if (needs + wants + savings) != 1:
            print("ERROR: Percentages must equal 100")
        else:
            self.data["percentNeeds"] = needs
            self.data["percentWants"] = wants
            self.data["percentSavings"] = savings
            
        
    def reset(self):
        '''Resets the user's data'''
        if input("Please enter 'y' to confirm: ").lower() == 'y':
            self.data = {
                "week" : 0,
                "income" : 0.0,
                "balanceNeeds" : 0.0,
                "balanceWants" : 0.0,
                "balanceSavings" : 0.0,
                "totalExpenses" : 0.0,
                "totalIncome" : 0.0
            }
            self._save()
            print("User data has been reset.")
        else:
            print("User data reset sequence has been aborted.")

    def start(self):
        '''Starts the application/runtime loop'''
        print("Welcome. Type 'help' to get started.")
        while True:
            try:
                self._readCommand(input(">> "))
            except KeyError:
                print("ERROR: That command does not exist. Please type 'help' for a list of commands.")
            except IndexError:
                print(f"ERROR: Not enough arguments for that command.")