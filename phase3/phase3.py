# DIMITRIOS PAGONIS 4985
# DIMITRIOS TZALOKOSTAS 4994


import string
import sys
import argparse
import os

class Token:
    def __init__(self, recognized_string, family, line_number):
        self.recognized_string = recognized_string
        self.family = family
        self.line_number = line_number
    
    def __repr__(self):
        return f"[{self.recognized_string} {self.family} {self.line_number}]"

class Lex:
    # characters and allowed symbols start
    greek_letters = ['α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ', 'μ', 
            'ν', 'ξ', 'ο', 'π', 'ρ', 'σ', 'τ', 'υ', 'φ', 'χ', 'ψ', 'ω','ς','Α', 'Β', 'Γ', 'Δ', 'Ε', 'Ζ', 'Η', 'Θ', 'Ι', 'Κ', 'Λ', 'Μ', 
            'Ν', 'Ξ', 'Ο', 'Π', 'Ρ', 'Σ', 'Τ', 'Υ', 'Φ', 'Χ', 'Ψ', 'Ω',
            'Ά', 'Έ', 'Ό', 'Ί', 'Ύ', 'Ή', 'Ώ', 'ά', 'ε', 'ό', 'ί', 'ύ', 'ή', 'ώ']
    english_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
            'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
            'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    addOperators = ['+', '-']
    mulOperators = ['*', '/']
    delimeters = [';', ',', '%']
    groupSymbols = ['(', ')', '[', ']']
    relationalOperators = ['<', '>', '=']
    assignents = [':', '=']
    multiTokens =[':=', '<=', '>=', '<>']
    logicalOperators = ['and', 'or', 'not']
    comments = ['{', '}'] # DEN EINAI TOKEN EINAI SXOLIO PREPEI NA AGNOHTHEI
    
    valid_characters = set(greek_letters + english_letters + numbers + addOperators + mulOperators + delimeters + groupSymbols + relationalOperators + assignents + comments)
    
    # characters end

    # edges start
    space             = 0 
    tab               = 1
    digit             = 2   
    greek_letter      = 3
    english_letter    = 4
    plus              = 5   #+
    minus             = 6   #- 
    mult              = 7   #*
    div               = 8   #/
    left_parenthesis  = 9   #(
    right_parenthesis = 10  #)
    left_aggili       = 11  #[
    right_aggili      = 12  #]
    koma              = 13  #,
    erotimatiko       = 14  #;
    mod               = 15  #%
    colon             = 16  #:
    equal             = 17  #=
    smaller           = 18  #<
    larger            = 19  #>
    anoigma_sxoliou   = 20  #{
    kleisimo_sxoliou  = 21  #}
    eof               = 22  #end of file
    kato_paula        = 23  #_
    other             = 24  #all other characters
    line_change       = 25  
    # edges end

    # states start
    start_state       = 0
    dig_state         = 1
    idk_state         = 2
    asgn_state        = 3
    lessthan_state    = 4
    greaterthan_state = 5
    rem_state         = 6
    # states end

    # tokens start
    number_token              = 100
    identifier_token          = 101
    keyword_token             = 102
    addOperator_token         = 103
    mulOperator_token         = 104
    delimeter_token           = 105
    groupSymbols_token        = 106
    relationalOperator_token  = 107
    assignent_token           = 108
    
    
    tokens = {
        number_token: "number",
        identifier_token: "identifier",
        keyword_token: "keyword",
        addOperator_token: "addOperator",
        mulOperator_token: "mulOperator",
        delimeter_token: "delimeter",
        groupSymbols_token: "groupSymbol",
        relationalOperator_token: "relationalOperator",
        assignent_token: "assignent"
    }
    # tokens end

    # keywords start
    keywords = [
        "πρόγραμμα", "δήλωση", "εάν", "τότε", "αλλιώς", "εάν_τέλος", "επανάλαβε", 
        "μέχρι", "όσο", "όσο_τέλος", "για", "έως", "με_βήμα", "για_τέλος", 
        "διάβασε", "γράψε", "συνάρτηση", "διαδικασία", "διαπροσωπεία", "είσοδος", 
        "έξοδος", "αρχή_συνάρτησης", "τέλος_συνάρτησης", "αρχή_διαδικασίας", 
        "τέλος_διαδικασίας", "αρχή_προγράμματος", "τέλος_προγράμματος", "ή", 
        "και", "όχι", "εκτέλεσε"
    ]
    # keywords end

    def __init__(self, current_line, file_name, token):
        self.current_line = current_line
        self.file_name = open(file_name, 'r', encoding='utf-8')
        self.token = token
        self.content = self.read_file_content(file_name)
        self.index = 0
        self.state = self.start_state
        self.readen_string = ''
        self.results = []
   
    def read_file_content(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
  
    def __del__(self):
        pass

    def error(self, readen_string, current_line):
        print(f"Lexical error at line {self.current_line}: {self.readen_string}")
        self.readen_string = self.readen_string[:-1]
        self.state = self.start_state
        
    
    def next_token(self, readen_string, next_state, line_number):
        # return Token object
        if self.check_keyword(self.readen_string):
            next_state = self.keyword_token

        token_family = self.tokens[next_state]
        return Token(self.readen_string, token_family, line_number)

    def check_keyword(self, string):
        if string in self.keywords:
            return True
        return False
    def resetStartState(self, readen_string,next_state, line_number):
        token = self.next_token(self.readen_string, next_state, self.current_line)
        self.readen_string = ''
        self.state = self.start_state
        self.results.append(token)
        return self.results
        
        
        
        

  
    def lex_states(self):
        self.state = self.start_state
        next_state = ''
        
        try:
            while self.index <= len(self.content):
                if self.index == len(self.content):
                    # Handle end of file
                   if self.state != self.start_state:
                        return self.resetStartState(self.readen_string, self.state, self.current_line)
                   else:
                        print("EOF reached")
                        break
                    

                chr = self.content[self.index]
                
                if self.state == self.start_state:
                    if chr == '\n':
                        self.current_line += 1
                    if chr.isspace():
                        next_state = self.start_state
                        self.index += 1
                        continue
                    elif chr.isdigit():
                        next_state = self.dig_state
                    elif chr.isalpha():
                        next_state = self.idk_state
                    elif chr in self.addOperators:
                        next_state = self.addOperator_token
                    elif chr in self.mulOperators:
                        next_state = self.mulOperator_token
                    elif chr in self.delimeters:
                        next_state = self.delimeter_token
                    elif chr in self.groupSymbols:
                        next_state = self.groupSymbols_token
                    elif chr in self.relationalOperators:
                        if chr == '<':
                           next_state = self.lessthan_state
                        elif chr == '>':
                            next_state = self.greaterthan_state
                        else:
                            next_state = self.relationalOperator_token
                    elif chr in self.assignents:
                        next_state = self.asgn_state
                    elif chr == '{':
                        next_state = self.rem_state
                        self.index += 1
                        if chr == '\n':
                            self.current_line += 1
                        self.state = next_state
                        next_state = ''
                        continue
                    
                    elif chr == '}': # error
                        self.readen_string += chr
                        self.error(self.readen_string, self.current_line)
                        #self.index += 1
                        if chr == '\n':
                            self.current_line += 1
                        
                        self.state = next_state
                        next_state = self.start_state
                        break
                    
                    elif chr == '_':
                        self.readen_string += chr
                        self.error(self.readen_string, self.current_line) #error
                        self.index+=1
                        break
                    
                    elif chr not in self.valid_characters:
                        self.readen_string += chr
                        self.error(self.readen_string, self.current_line) #error
                        self.index += 1
                        break
                    
                    # PROTA DIAVASE META GRAPSE
                    if next_state != self.start_state or next_state != self.rem_state:
                        self.readen_string += chr
                    
                
                elif self.state == self.dig_state:
                    
                    if chr.isdigit():
                        self.readen_string += chr
                        next_state = self.dig_state
                    elif chr.isalpha():
                        
                        self.readen_string += chr
                        self.error(self.readen_string, self.current_line)
                        break
                        
                    else:
                        next_state = self.number_token
                        return self.resetStartState(self.readen_string, next_state, self.current_line)
                        
                elif self.state == self.idk_state:
                    if chr.isalpha() or chr.isdigit() or chr == '_':
                        self.readen_string += chr
                        
                        next_state = self.idk_state
                    else:
                        next_state = self.identifier_token
                        #print ('returns',self.resetStartState(self.readen_string, next_state, self.current_line))
                        return self.resetStartState(self.readen_string, next_state, self.current_line)

                elif self.state == self.addOperator_token:
                    
                    next_state = self.addOperator_token
                    return self.resetStartState(self.readen_string, next_state, self.current_line)
                    #continue

                elif self.state == self.mulOperator_token:
                    
                    next_state = self.mulOperator_token
                    return self.resetStartState(self.readen_string, next_state, self.current_line)
                    #continue

                elif self.state == self.delimeter_token:
                    
                    next_state = self.delimeter_token
                    return self.resetStartState(self.readen_string, next_state, self.current_line)
                    #continue

                elif self.state == self.groupSymbols_token:
                    
                    next_state = self.groupSymbols_token
                    return self.resetStartState(self.readen_string, next_state, self.current_line)
                    #continue


                elif self.state == self.lessthan_state:
                    
                    if chr in self.valid_characters and self.readen_string + chr not in self.multiTokens:
                        next_state = self.relationalOperator_token
                        return self.resetStartState(self.readen_string, next_state, self.current_line)
                        
                        #continue
                    elif self.readen_string + chr in self.multiTokens:
                        self.readen_string += chr
                        next_state = self.relationalOperator_token
                        self.index += 1
                        return self.resetStartState(self.readen_string, next_state, self.current_line)
                        #continue
                
                    else:
                        
                        self.error(self.readen_string, self.current_line)
                        break


                elif self.state == self.greaterthan_state:
                    if chr in self.valid_characters and self.readen_string + chr not in self.multiTokens:
                        next_state = self.relationalOperator_token
                        return self.resetStartState(self.readen_string, next_state, self.current_line)
                        
                        #continue
                    elif self.readen_string + chr in self.multiTokens:
                        self.readen_string += chr
                        next_state = self.relationalOperator_token
                        self.index += 1
                        return self.resetStartState(self.readen_string, next_state, self.current_line)
                        #continue
                    else:
                        self.error(self.readen_string, self.current_line)
                        break

                elif self.state == self.relationalOperator_token:
                    # Αν το επόμενο char φτιάχνει multi-token (<=, >=, <>)
                    if self.readen_string + chr in self.multiTokens:
                        self.readen_string += chr
                        next_state = self.relationalOperator_token
                        self.index += 1
                        return self.resetStartState(self.readen_string, next_state, self.current_line)
                     # Αν το επόμενο char είναι ψηφίο ή γράμμα ή κενό ή οτιδήποτε άλλο, τελείωσε το token εδώ!
                    else:
                        next_state = self.relationalOperator_token
                        return self.resetStartState(self.readen_string, next_state, self.current_line)
                elif self.state == self.asgn_state:
                    ##if chr in self.valid_characters and self.readen_string + chr not in self.multiTokens:
                        ##next_state = self.relationalOperator_token
                        ##self.resetStartState(self.readen_string, next_state, self.current_line)
                        
                        ##continue
                    if self.readen_string + chr in self.multiTokens:
                        self.readen_string += chr
                        next_state = self.assignent_token
                        self.index += 1
                        return self.resetStartState(self.readen_string, next_state, self.current_line)
                        #continue
                    else: #error
                        self.error(self.readen_string, self.current_line)
                        break
                elif self.state == self.rem_state:
                    if chr == '}':
                        next_state = self.start_state
                        
                    else:
                        next_state = self.rem_state
                    if chr == '\n':
                        self.current_line += 1
                
                # DES PROTA AYTO BEFORE TOKENS
                self.index += 1
                self.state = next_state
                next_state = ''

                if len(self.readen_string) > 30:
                    self.error(self.readen_string, self.current_line)
                    print("Length out of range")
                    break
            
        except Exception as e:
            print(e)
        
       
## 2nd Phase ENDIAMESOS KWDIKAS ##
## genQuad newTemp backPatch na einai diaforetika ##


### PINAKAS SYMBOLWN ####

class SymbolTable:
    def __init__(self):
        self.allSymbolsList = [] ## edo einai o pinakas
        self.entity = self.Entity()
        self.scope = self.Scope()
        self.argument = self.Argument()
        self.endiamesos = EndiamesosKwdikas()

       
    
    class Entity: #orthogwnio
        def __init__(self):
            self.outputFile = ''
            self.name = ''
            self.entityType = '' ##ti ontothta einai
            self.variable = self.Variable()
            self.funcorproc = self.FuncOrProc()
            self.parameter = self.Parameter()
            self.tmpvariable = self.tmpVariable()

        class Variable:
            def __init__(self):
                self.type = ''
                self.offset = 0
        
        class FuncOrProc:

            def __init__(self):
                self.type = ''
                self.startQuad = 0
                self.arguments = []
                self.frameLength = 0
        
        class Parameter:
            
            def __init__(self):
                self.parMode = 0
                self.offset = 0

        ##class Constant:
           ## def __init__(self):

        
        class tmpVariable:

            def __init__(self):
                self.type = ''
                self.offset = 0
            
    class Scope: #kyklos

        def __init__(self):
            self.name = ''
            self.entityList = []
            self.nestingLevel = 0


    class Argument: #trigwno

        def __init__(self):
            self.name = ''
            self.parMode = ''
            self.type = ''
    
    def new_argument(self, new_arg):

        self.allSymbolsList[-1].entityList[-1].funcorproc.arguments.append(new_arg)
    
    def new_entity(self, new_entity):
        
        self.allSymbolsList[-1].entityList.append(new_entity)
    
    def new_scope(self, newScope):

        tmp = self.Scope()
        tmp.name = newScope

        tmp.nestingLevel = (self.allSymbolsList[-1].nestingLevel + 1) if self.allSymbolsList else 0

        self.allSymbolsList.append(tmp)
    
    def delete_scope(self):
        
        if self.allSymbolsList:
            removedScope = self.allSymbolsList.pop()

            del removedScope
    
    def compute_offset(self):

        count = 0
        
        if not self.allSymbolsList or not self.allSymbolsList[-1].entityList:
            return 12 

        count = sum(1 for ent in self.allSymbolsList[-1].entityList if ent.entityType in ('VAR', 'TEMP', 'PARAM'))

        return 12 + count * 4

    def compute_startQuad(self):
        

        if len(self.allSymbolsList) > 1:
            self.allSymbolsList[-2].entityList[-1].funcorproc.startQuad = self.endiamesos.nextQuad()


    def compute_framelength(self):

        self.allSymbolsList[-2].entityList[-1].funcorproc.frameLength = self.compute_offset()
    
    def add_parameters(self):

        for i in self.allSymbolsList[-2].entityList[-1].funcorproc.arguments:
            ent = self.Entity()
            ent.name = i.name
            ent.entityType = 'PARAM'
            ent.parameter.parMode = i.parMode
            ent.parameter.offest = self.compute_offset()
            self.new_entity(ent)
    
   
        

class EndiamesosKwdikas:
    
    def __init__(self):
        self.total_quads = []
        self.count = 1
        self.T_i = 1

    
    def nextQuad(self):
        
        return self.count
    
    def genQuad(self, one, two, three, four):
        quad = [self.nextQuad(), one, two, three, four] #dhmioyrgia 4adas
        print(f"[DEBUG] genQuad: {quad}") #DEBUG
        self.total_quads.append(quad)
        self.count += 1
        return quad
    
    def newTemp(self, pinakas):
        
        tmp = "T_"+ str(self.T_i)
        self.T_i +=1

        ent = pinakas.Entity()
        ent.entityType = 'TEMP'
        ent.name = tmp
        ent.tmpvariable.type = 'Int'
        ent.tmpvariable.offset = pinakas.compute_offset()
        pinakas.new_entity(ent)

        return tmp
    
    def emptyList(self):
        
        return []
    
    def makeList(self, x):
        
        return [x]

    def merge(self, i, j):

        return (i + j)

    def backPatch(self, l, label_target):
        # to l einai lista me deiktes pou deixnoyn poia quads den einai symplhrwmena 

        for quad_index in l:
            for quad in self.total_quads:
                if quad[0] == quad_index and quad[-1] == '_':
                    quad[-1] = label_target
                    break
        return 



class Syntaktikos:
    def __init__(self, line_number, file_path, token):
        self.line_number = line_number
        self.file_path = file_path
        self.token = token
        self.lexer = Lex(line_number, file_path, token)
        self.lexer_results = []
        self.endiamesos = EndiamesosKwdikas()
        self.pinakasSymvolwn = SymbolTable()
        
        self.outputIntFile = open('intFile.int', 'w', encoding='utf-8')
        self.outputSymFile = open('symbolFile.sym', 'w', encoding='utf-8')
        self.count = 1
        self.outputAsmFile = open('asc_file.asm', 'w', encoding='utf-8')
        self.final = Final(self.pinakasSymvolwn.allSymbolsList, self.endiamesos.total_quads, self.outputAsmFile)
        self.seira = -1
        self.program()

        self.final_code()

        self.intCode(self.outputIntFile)
        self.outputIntFile.close()
        self.outputSymFile.write("SYMBOL TABLE has been completed\n")
        self.outputSymFile.close()
        

    def program(self):
        self.lexer_results = self.lexer.lex_states()
        if not self.lexer_results:
            print("ERROR: No tokens found")
            exit(-1)

        if self.lexer_results[-1].family == "keyword" and self.lexer_results[-1].recognized_string == "πρόγραμμα":
            self.lexer_results = self.lexer.lex_states()
            current_string = self.lexer_results[-1].recognized_string
            if self.lexer_results and self.lexer_results[-1].family == "identifier":
                self.lexer_results = self.lexer.lex_states()
                
                self.programblock(current_string)
                
                
            else:
                print(f"ERROR: Δεν υπάρχει onoma programmatos, line {self.lexer_results[-1].line_number}")
                exit(-1)
        else:
            print(f"ERROR: H leksi 'πρόγραμμα' Δεν υπάρχει stin arxi tou programmatos, line {self.lexer_results[-1].line_number}")
            exit(-1)


    def programblock(self, name):
        
        self.pinakasSymvolwn.new_scope(name)
        
        
        self.declarations()
        self.subprograms()
        #self.lexer_results = self.lexer.lex_states()
        
        
        
       

        if self.lexer_results and self.lexer_results[-1].family == "keyword" and self.lexer_results[-1].recognized_string == "αρχή_προγράμματος":
            self.lexer_results = self.lexer.lex_states()
            
            self.endiamesos.genQuad('begin_block', name, '_', '_')
            self.sequence()
            self.endiamesos.genQuad('halt','_','_','_')
            self.endiamesos.genQuad('end_block',name,'_','_')
            
            self.symTable(self.outputSymFile)
            
            self.final_code()
            
            self.pinakasSymvolwn.delete_scope()

            if self.lexer_results[-1].family == "keyword" and self.lexer_results[-1].recognized_string == "τέλος_προγράμματος":
                self.lexer_results = self.lexer.lex_states()
                
            else:
                print(f"ERROR: Δεν υπάρχει leksi 'τέλος_προγράμματος', line {self.lexer_results[-1].line_number}")
                exit(-1)
        else:
            print(f"ERROR: Δεν υπάρχει leksi 'αρχή_προγράμματος', line {self.lexer_results[-1].line_number}")
            exit(-1)

        
        
    def declarations(self):
       while self.lexer_results and self.lexer_results[-1].family == "keyword" and self.lexer_results[-1].recognized_string == "δήλωση":
            self.lexer_results = self.lexer.lex_states()
            self.varlist_declarations()
            
    def varlist_declarations(self):
        """Handles variable declarations"""
        if self.lexer_results and self.lexer_results[-1].family == "identifier":
            id = self.lexer_results[-1].recognized_string
            self.lexer_results = self.lexer.lex_states()

            # Create an Entity for the variable
            ent = self.pinakasSymvolwn.Entity()
            ent.entityType = 'VAR'
            ent.name = id
            ent.variable.type = 'Int'  
            ent.variable.offset = self.pinakasSymvolwn.compute_offset()
            self.pinakasSymvolwn.new_entity(ent)

            # Handle comma-separated identifiers
            while self.lexer_results and self.lexer_results[-1].family == "delimeter" and self.lexer_results[-1].recognized_string == ',':
                self.lexer_results = self.lexer.lex_states()
                if self.lexer_results and self.lexer_results[-1].family == "identifier":
                    id = self.lexer_results[-1].recognized_string
                    self.lexer_results = self.lexer.lex_states()

                    # Create an Entity for each variable
                    ent = self.pinakasSymvolwn.Entity()
                    ent.entityType = 'VAR'
                    ent.name = id
                    ent.variable.offset = self.pinakasSymvolwn.compute_offset()
                    self.pinakasSymvolwn.new_entity(ent)
                else:
                    print(f"ERROR: Δεν υπάρχει όνομα μεταβλητής μετά το κόμμα, line {self.lexer_results[-1].line_number}")
                    exit(-1)
        else:
            print(f"ERROR: Δεν υπάρχει όνομα μεταβλητής, line {self.lexer_results[-1].line_number}")
            exit(-1)


    def varlist_formalparlist(self):
            """Handles formal parameter lists."""
            if self.lexer_results and self.lexer_results[-1].family == "identifier":
                id = self.lexer_results[-1].recognized_string
                self.lexer_results = self.lexer.lex_states()

                # Create an Argument for the parameter
                arg = self.pinakasSymvolwn.Argument()
                arg.name = id
                arg.parMode = ''  # Mode will be updated later
                arg.type = 'Int'  
                self.pinakasSymvolwn.new_argument(arg)

                # Handle comma-separated identifiers
                while self.lexer_results and self.lexer_results[-1].family == "delimeter" and self.lexer_results[-1].recognized_string == ',':
                    self.lexer_results = self.lexer.lex_states()
                    if self.lexer_results and self.lexer_results[-1].family == "identifier":
                        id = self.lexer_results[-1].recognized_string
                        self.lexer_results = self.lexer.lex_states()

                        # Create an Argument for each parameter
                        arg = self.pinakasSymvolwn.Argument()
                        arg.name = id
                        arg.parMode = ''  # Mode will be updated later
                        arg.type = 'Int'
                        self.pinakasSymvolwn.new_argument(arg)
                    else:
                        print(f"ERROR: Δεν υπάρχει όνομα παραμέτρου μετά το κόμμα, line {self.lexer_results[-1].line_number}")
                        exit(-1)
            else:
                print(f"ERROR: Δεν υπάρχει όνομα παραμέτρου, line {self.lexer_results[-1].line_number}")
                exit(-1)


    def varlist_funcinput(self):
        """Handles input parameters for functions."""
        if self.lexer_results and self.lexer_results[-1].family == "identifier":
            id = self.lexer_results[-1].recognized_string
            self.lexer_results = self.lexer.lex_states()

            # Update the parameter mode to CV (Call by Value)
            for arg in self.pinakasSymvolwn.allSymbolsList[-1].entityList[-1].funcorproc.arguments:
                if arg.name == id:
                    arg.parMode = 'CV'

            # Handle comma-separated identifiers
            while self.lexer_results and self.lexer_results[-1].family == "delimeter" and self.lexer_results[-1].recognized_string == ',':
                self.lexer_results = self.lexer.lex_states()
                if self.lexer_results and self.lexer_results[-1].family == "identifier":
                    id = self.lexer_results[-1].recognized_string
                    self.lexer_results = self.lexer.lex_states()

                    # Update the parameter mode to CV for each identifier
                    for arg in self.pinakasSymvolwn.allSymbolsList[-1].entityList[-1].funcorproc.arguments:
                        if arg.name == id:
                            arg.parMode = 'CV'
                else:
                    print(f"ERROR: Δεν υπάρχει όνομα παραμέτρου εισόδου μετά το κόμμα, line {self.lexer_results[-1].line_number}")
                    exit(-1)
        else:
            print(f"ERROR: Δεν υπάρχει όνομα παραμέτρου εισόδου, line {self.lexer_results[-1].line_number}")
            exit(-1)


    def varlist_funcoutput(self):
        """Handles output parameters for functions."""
        if self.lexer_results and self.lexer_results[-1].family == "identifier":
            id = self.lexer_results[-1].recognized_string
            self.lexer_results = self.lexer.lex_states()

            # Update the parameter mode to REF (Call by Reference)
            for arg in self.pinakasSymvolwn.allSymbolsList[-1].entityList[-1].funcorproc.arguments:
                if arg.name == id:
                    arg.parMode = 'REF'

            # Handle comma-separated identifiers
            while self.lexer_results and self.lexer_results[-1].family == "delimeter" and self.lexer_results[-1].recognized_string == ',':
                self.lexer_results = self.lexer.lex_states()
                if self.lexer_results and self.lexer_results[-1].family == "identifier":
                    id = self.lexer_results[-1].recognized_string
                    self.lexer_results = self.lexer.lex_states()

                    # Update the parameter mode to REF for each identifier
                    for arg in self.pinakasSymvolwn.allSymbolsList[-1].entityList[-1].funcorproc.arguments:
                        if arg.name == id:
                            arg.parMode = 'REF'
                else:
                    print(f"ERROR: Δεν υπάρχει όνομα παραμέτρου εξόδου μετά το κόμμα, line {self.lexer_results[-1].line_number}")
                    exit(-1)
        else:
            print(f"ERROR: Δεν υπάρχει όνομα παραμέτρου εξόδου, line {self.lexer_results[-1].line_number}")
            exit(-1)
        

    def subprograms(self):
        
        while self.lexer_results and (self.lexer_results[-1].family == "keyword" and (self.lexer_results[-1].recognized_string == "συνάρτηση" or self.lexer_results[-1].recognized_string == "διαδικασία")):
            if self.lexer_results[-1].recognized_string == "συνάρτηση":
                self.func()
            else:
                self.proc()
    
    def func(self):
        
        
        if self.lexer_results and self.lexer_results[-1].family == "keyword" and self.lexer_results[-1].recognized_string == "συνάρτηση":
            self.lexer_results = self.lexer.lex_states()
            if self.lexer_results and self.lexer_results[-1].family == "identifier":
                current_string = self.lexer_results[-1].recognized_string
                self.lexer_results = self.lexer.lex_states()
                
                if self.lexer_results and self.lexer_results[-1].recognized_string == '(':
                    self.lexer_results = self.lexer.lex_states()
                    ent = self.pinakasSymvolwn.Entity()						
                    ent.entityType = 'SUBPR'				
                    ent.name = current_string					
                    ent.funcorproc.type = 'Function'	
                    self.pinakasSymvolwn.new_entity(ent)
                    
                    self.formalparlist()

                    if self.lexer_results and self.lexer_results[-1].recognized_string == ')':
                        self.lexer_results = self.lexer.lex_states()
                        self.funcblock(current_string)
                    else:
                        print(f"ERROR: Den kleinei h deksia parenthesi meta thn formalparlist, line {self.lexer_results[-1].line_number}")
                        exit(-1)
                else:
                    print(f"ERROR: Den anoigei h aristeri parenthesi prin thn formalparlist, line {self.lexer_results[-1].line_number}")
                    exit(-1)
            else:
                print(f"ERROR: Perimenoume to id meta to function, line {self.lexer_results[-1].line_number}")
                exit(-1)
        else:
            print(f"ERROR: Δεν υπάρχει function, line {self.lexer_results[-1].line_number}")
            exit(-1)

    def proc(self):
        
        if self.lexer_results and self.lexer_results[-1].family == "keyword" and self.lexer_results[-1].recognized_string == "διαδικασία":
            self.lexer_results = self.lexer.lex_states()
            if self.lexer_results and self.lexer_results[-1].family == "identifier":
                current_string = self.lexer_results[-1].recognized_string
                self.lexer_results = self.lexer.lex_states()
                if self.lexer_results and self.lexer_results[-1].recognized_string == '(':
                    self.lexer_results = self.lexer.lex_states()
                    ent = self.pinakasSymvolwn.Entity()						
                    ent.entityType = 'SUBPR'				
                    ent.name = current_string					
                    ent.funcorproc.type = 'Procedure'	
                    self.pinakasSymvolwn.new_entity(ent)
                    
                    self.formalparlist()
                    if self.lexer_results and self.lexer_results[-1].recognized_string == ')':
                        self.lexer_results = self.lexer.lex_states()
                        self.procblock(current_string)
                    else:
                        print(f"ERROR: Den kleinei h deksia parenthesi meta thn formalparlist, line {self.lexer_results[-1].line_number}")
                        exit(-1)
                else:
                    print(f"ERROR: Den anoigei h aristeri parenthesi prin thn formalparlist, line {self.lexer_results[-1].line_number}")
                    exit(-1)
            else:
                print(f"ERROR: Perimenoume to id meta to procedure, line {self.lexer_results[-1].line_number}")
                exit(-1)


    def formalparlist(self):
        

        if self.lexer_results and self.lexer_results[-1].family == "identifier":
            self.varlist_formalparlist()
        else:
            print(f"ERROR: Δεν υπάρχει id sti formalparlist, line {self.lexer_results[-1].line_number}")
            exit(-1)

    def funcblock(self, name):
        
        if self.lexer_results and self.lexer_results[-1].family == "keyword" and self.lexer_results[-1].recognized_string == "διαπροσωπεία":
            self.lexer_results = self.lexer.lex_states()
            self.funcinput()
            self.funcoutput()
            
            self.pinakasSymvolwn.new_scope(name)
            self.pinakasSymvolwn.add_parameters()
            
            self.declarations()
            self.subprograms()
            if self.lexer_results and self.lexer_results[-1].family == "keyword" and self.lexer_results[-1].recognized_string == "αρχή_συνάρτησης":
                self.lexer_results = self.lexer.lex_states()

                self.pinakasSymvolwn.compute_startQuad()
                self.endiamesos.genQuad('begin_block', name, '_', '_')
                self.sequence()
                self.pinakasSymvolwn.compute_framelength()
                self.endiamesos.genQuad('end_block', name, '_', '_')
                self.symTable(self.outputSymFile)
                
                self.final_code()
                
                self.pinakasSymvolwn.delete_scope()
                if self.lexer_results[-1].family == "keyword" and self.lexer_results[-1].recognized_string == "τέλος_συνάρτησης":
                    self.lexer_results = self.lexer.lex_states()
                else:
                    print(f"ERROR: H leksi 'τέλος_συνάρτησης' Δεν υπάρχει sto telos tis sinartisis, line {self.lexer_results[-1].line_number}")
                    exit(-1)
            else:
                print(f"ERROR: H leksi 'αρχή_συνάρτησης' Δεν υπάρχει stin arxi tis sinartisis, line {self.lexer_results[-1].line_number}")
                exit(-1)
        else:
            print(f"ERROR: H leksi 'διαπροσωπεία' Δεν υπάρχει stin arxi tis sinartisis, line {self.lexer_results[-1].line_number}")
            exit(-1)

    
    
    
    def procblock(self, name):
        if self.lexer_results and self.lexer_results[-1].family == "keyword" and self.lexer_results[-1].recognized_string == "διαπροσωπεία":
            self.lexer_results = self.lexer.lex_states()
            self.funcinput()
            self.funcoutput()
            self.pinakasSymvolwn.new_scope(name)
            self.pinakasSymvolwn.add_parameters()
            self.declarations()
            self.subprograms()
            if self.lexer_results and self.lexer_results[-1].family == "keyword" and self.lexer_results[-1].recognized_string == "αρχή_διαδικασίας":
                self.lexer_results = self.lexer.lex_states()

                self.pinakasSymvolwn.compute_startQuad()
                self.endiamesos.genQuad('begin_block', name, '_', '_')
                self.sequence()
                self.pinakasSymvolwn.compute_framelength()
                self.endiamesos.genQuad('end_block',name,'_','_')

                self.symTable(self.outputSymFile)
                
                self.final_code()
                
                self.pinakasSymvolwn.delete_scope()
                
                if self.lexer_results[-1].family == "keyword" and self.lexer_results[-1].recognized_string == "τέλος_διαδικασίας":
                    self.lexer_results = self.lexer.lex_states()
                else:
                    print(f"ERROR: H leksi 'τέλος_διαδικασίας' Δεν υπάρχει sto telos tis diadikasias, line {self.lexer_results[-1].line_number}")
                    exit(-1)
            else:
                print(f"ERROR: H leksi 'αρχή_διαδικασίας' Δεν υπάρχει stin arxi tis diadikasias, line {self.lexer_results[-1].line_number}")
                exit(-1)
        else:
                print(f"ERROR: H leksi 'διαπροσωπεία' Δεν υπάρχει stin arxi tis diadikasias, line {self.lexer_results[-1].line_number}")
                exit(-1)


        
    def funcinput(self):
        
        if self.lexer_results[-1].family == "keyword" and self.lexer_results[-1].recognized_string == "είσοδος":
            self.lexer_results = self.lexer.lex_states()
            self.varlist_funcinput()


    def funcoutput(self):
        
        if self.lexer_results[-1].family == "keyword" and self.lexer_results[-1].recognized_string == "έξοδος":
            self.lexer_results = self.lexer.lex_states()
            self.varlist_funcoutput()

    def sequence(self):
       
        self.statement()
        while self.lexer_results and self.lexer_results[-1].family == "delimeter" and self.lexer_results[-1].recognized_string == ';':
            self.lexer_results = self.lexer.lex_states()
            self.statement()

    def statement(self):
       
        if not self.lexer_results:
            print("ERROR: No tokens available")
            exit(-1)
        if self.lexer_results[-1].family == "identifier":
            self.assignment_stat()
        elif self.lexer_results[-1].family == "keyword" and self.lexer_results[-1].recognized_string == "εάν":
            self.if_stat()
        elif self.lexer_results[-1].family == "keyword" and self.lexer_results[-1].recognized_string == "όσο":
            self.while_stat()
        elif self.lexer_results[-1].family == "keyword" and self.lexer_results[-1].recognized_string == "επανάλαβε":
            self.do_stat()
        elif self.lexer_results[-1].family == "keyword" and self.lexer_results[-1].recognized_string == "για":
            self.for_stat()
        elif self.lexer_results[-1].family == "keyword" and self.lexer_results[-1].recognized_string == "διάβασε":
            self.input_stat()
        elif self.lexer_results[-1].family == "keyword" and self.lexer_results[-1].recognized_string == "γράψε":
            self.print_stat()
        elif self.lexer_results[-1].family == "keyword" and self.lexer_results[-1].recognized_string == "εκτέλεσε":
            self.call_stat()
        else:
            print(f"ERROR: H εντολή που δώσατε δεν ανήκει στη γλώσσα, line {self.lexer_results[-1].line_number}")
            exit(-1)
    
    def assignment_stat(self):
        
        if not self.lexer_results:
            print("ERROR: No tokens available")
            exit(-1)
            
        if self.lexer_results[-1].family == "identifier":
            current_string = self.lexer_results[-1].recognized_string
            self.lexer_results = self.lexer.lex_states()
            
            if self.lexer_results and self.lexer_results[-1].recognized_string == ":=":
                self.lexer_results = self.lexer.lex_states()
                E_place = self.expression()
                self.endiamesos.genQuad(':=', E_place, '_', current_string)
            else:
                print(f"ERROR: Πρέπει να υπάρχει το σύνολο ανάθεσης μετα το όνομα της μεταβλητής, line {self.lexer_results[-1].line_number} στο {self.lexer_results[-1].recognized_string}")
                exit(-1)
        else:
            print(f"ERROR: Δεν υπάρχει το όνομα μεταβλητής, line {self.lexer_results[-1].line_number} στο {self.lexer_results[-1].recognized_string}")
            exit(-1)
    
    def if_stat(self):
        if not self.lexer_results:
            
            exit(-1)

        if self.lexer_results[-1].family == "keyword" and self.lexer_results[-1].recognized_string == "εάν":
            self.lexer_results = self.lexer.lex_states()
            
            condition = self.condition()
            self.endiamesos.backPatch(condition[0], self.endiamesos.nextQuad())

            if self.lexer_results and self.lexer_results[-1].recognized_string == "τότε":
                self.lexer_results = self.lexer.lex_states()
                self.sequence()

                if_list = self.endiamesos.makeList(self.endiamesos.nextQuad())
                self.endiamesos.genQuad('jump', '_', '_', '_')
                self.endiamesos.backPatch(condition[1], self.endiamesos.nextQuad())
                self.elsepart()

                self.endiamesos.backPatch(if_list, self.endiamesos.nextQuad())

                if self.lexer_results and self.lexer_results[-1].recognized_string == "εάν_τέλος":
                    self.lexer_results = self.lexer.lex_states()
                else:
                    print(f"ERROR: Δεν υπάρχει 'εάν_τέλος', line {self.lexer_results[-1].line_number} στο {self.lexer_results[-1].recognized_string} ")
                    exit(-1)
            else:
                print(f"ERROR: Δεν υπάρχει 'τότε', line {self.lexer_results[-1].line_number} στο {self.lexer_results[-1].recognized_string}")
                exit(-1)
        else:
            print(f"ERROR: Δεν υπάρχει 'εάν', line {self.lexer_results[-1].line_number} στο {self.lexer_results[-1].recognized_string}")
            exit(-1)
    def elsepart(self):
        
        if not self.lexer_results:
            print("ERROR: No tokens available")
            exit(-1)

        if self.lexer_results[-1].family == "keyword" and self.lexer_results[-1].recognized_string == "αλλιώς":
            self.lexer_results = self.lexer.lex_states()
            self.sequence()
    def while_stat(self):
    
        if not self.lexer_results:
            print("ERROR: No tokens available")
            exit(-1)

        if self.lexer_results[-1].family == "keyword" and self.lexer_results[-1].recognized_string == "όσο":
            self.lexer_results = self.lexer.lex_states()
            
            current_quad = self.endiamesos.nextQuad()
            condition = self.condition()

            self.endiamesos.backPatch(condition[0], self.endiamesos.nextQuad())

            if self.lexer_results and self.lexer_results[-1].recognized_string == "επανάλαβε":
                self.lexer_results = self.lexer.lex_states()
                self.sequence()

                self.endiamesos.genQuad('jump', '_', '_', current_quad)
                self.endiamesos.backPatch(condition[1], self.endiamesos.nextQuad())

                if self.lexer_results and self.lexer_results[-1].recognized_string == "όσο_τέλος":
                    self.lexer_results = self.lexer.lex_states()
                else:
                    print(f"ERROR: Δεν υπάρχει 'όσο_τέλος', line {self.lexer_results[-1].line_number} στο {self.lexer_results[-1].recognized_string}")
                    exit(-1)
            else:
                print(f"ERROR: Δεν υπάρχει 'επανάλαβε', line {self.lexer_results[-1].line_number} στο {self.lexer_results[-1].recognized_string}")
                exit(-1)
    def do_stat(self):
        if not self.lexer_results:
            print("ERROR: No tokens available")
            exit(-1)

        if self.lexer_results[-1].family == "keyword" and self.lexer_results[-1].recognized_string == "επανάλαβε":
            self.lexer_results = self.lexer.lex_states()
            
            current_quad = self.endiamesos.nextQuad()

            self.sequence()

            if self.lexer_results and self.lexer_results[-1].recognized_string == "μέχρι":
                self.lexer_results = self.lexer.lex_states()

                condition = self.condition()

                self.endiamesos.backPatch(condition[1], current_quad)
                self.endiamesos.backPatch(condition[0], self.endiamesos.nextQuad())

            else:
                print(f"ERROR: Δεν υπάρχει 'μέχρι', line {self.lexer_results[-1].line_number} στο {self.lexer_results[-1].recognized_string}")
                exit(-1)
    
    def for_stat(self):
        if not self.lexer_results:
            print("ERROR: No tokens available")
            exit(-1)

        if self.lexer_results[-1].family == "keyword" and self.lexer_results[-1].recognized_string == "για":
            self.lexer_results = self.lexer.lex_states()
            if self.lexer_results and self.lexer_results[-1].family == "identifier":
                id_rec_string = self.lexer_results[-1].recognized_string
                self.lexer_results = self.lexer.lex_states()
                if self.lexer_results and self.lexer_results[-1].recognized_string == ":=":
                    self.lexer_results = self.lexer.lex_states()
                    E_place1 = self.expression()

                    self.endiamesos.genQuad(':=', E_place1, '_', id_rec_string)
                    
                    if self.lexer_results and self.lexer_results[-1].recognized_string == "έως":
                        self.lexer_results = self.lexer.lex_states()
                        E_place2 = self.expression()
                        if self.lexer_results and self.lexer_results[-1].recognized_string == "με_βήμα":
                            step = self.step()
                            current_quad = self.endiamesos.nextQuad()

                            L_thetiko = self.endiamesos.makeList(self.endiamesos.nextQuad())
                            self.endiamesos.genQuad('>', step, '0', '_')
                            L_arnhtiko = self.endiamesos.makeList(self.endiamesos.nextQuad())
                            self.endiamesos.genQuad('<', step, '0', '_')
                            L_mhden = self.endiamesos.makeList(self.endiamesos.nextQuad())
                            self.endiamesos.genQuad('=', step, '0', '_')

                            self.endiamesos.backPatch(L_thetiko, self.endiamesos.nextQuad())
                            L_thetiko_out = self.endiamesos.makeList(self.endiamesos.nextQuad())
                            self.endiamesos.genQuad('>=', id_rec_string, E_place2, '_')
                            L_thetiko_in = self.endiamesos.makeList(self.endiamesos.nextQuad())
                            self.endiamesos.genQuad('jump', '_', '_', '_')

                            self.endiamesos.backPatch(L_arnhtiko, self.endiamesos.nextQuad())
                            L_arnhtiko_out = self.endiamesos.makeList(self.endiamesos.nextQuad())
                            self.endiamesos.genQuad('<=', id_rec_string, E_place2, '_')
                            L_arnhtiko_in = self.endiamesos.makeList(self.endiamesos.nextQuad())
                            self.endiamesos.genQuad('jump', '_', '_', '_')

                            

                            self.endiamesos.backPatch(L_mhden, self.endiamesos.nextQuad())



                            if self.lexer_results and self.lexer_results[-1].recognized_string == "επανάλαβε":
                                self.lexer_results = self.lexer.lex_states()

                                self.endiamesos.backPatch(L_thetiko_in, self.endiamesos.nextQuad())
                                self.endiamesos.backPatch(L_arnhtiko_in, self.endiamesos.nextQuad())

                                self.sequence()

                                self.endiamesos.genQuad('+', id_rec_string, step, id_rec_string)
                                self.endiamesos.genQuad('jump', '_', '_', current_quad)

                                self.endiamesos.backPatch(L_thetiko_out, self.endiamesos.nextQuad())
                                self.endiamesos.backPatch(L_arnhtiko_out, self.endiamesos.nextQuad())

                                if self.lexer_results and self.lexer_results[-1].recognized_string == "για_τέλος":
                                    self.lexer_results = self.lexer.lex_states()
                                else:
                                    print(f"ERROR: Δεν υπάρχει 'για_τέλος', line {self.lexer_results[-1].line_number} στο {self.lexer_results[-1].recognized_string}")
                                    exit(-1)
                            else:
                                print(f"ERROR: Δεν υπάρχει 'επανάλαβε', line {self.lexer_results[-1].line_number} στο {self.lexer_results[-1].recognized_string}")
                                exit(-1)
                        else:
                            print(f"ERROR: Δεν υπάρχει 'με_βήμα', line {self.lexer_results[-1].line_number} στο {self.lexer_results[-1].recognized_string}")
                            exit(-1)
                    else:
                        print(f"ERROR: Δεν υπάρχει 'έως', line {self.lexer_results[-1].line_number} στο {self.lexer_results[-1].recognized_string}")
                        exit(-1)
                else:
                    print(f"ERROR: Δεν υπάρχει ':=', line {self.lexer_results[-1].line_number} στο {self.lexer_results[-1].recognized_string}")
                    exit(-1)
            else:
                print(f"ERROR: Δεν υπάρχει id, line {self.lexer_results[-1].line_number} στο {self.lexer_results[-1].recognized_string}")
                exit(-1)
    def step(self):
        if not self.lexer_results:
            print("ERROR: No tokens available")
            exit(-1)
        if self.lexer_results[-1].family == "keyword" and self.lexer_results[-1].recognized_string == "με_βήμα":
            self.lexer_results = self.lexer.lex_states()
            return self.expression()
        return '1'
       

    
    def print_stat(self):
       
        if not self.lexer_results:
            print("ERROR: No tokens available")
            exit(-1)

        if self.lexer_results[-1].family == "keyword" and self.lexer_results[-1].recognized_string == "γράψε":
            self.lexer_results = self.lexer.lex_states()
            E_place = self.expression()
            self.endiamesos.genQuad('out', E_place, '_', '_')
        
    def input_stat(self):
       
        if not self.lexer_results:
            print("ERROR: No tokens available")
            exit(-1)

        if self.lexer_results[-1].family == "keyword" and self.lexer_results[-1].recognized_string == "διάβασε":
            self.lexer_results = self.lexer.lex_states()
            if self.lexer_results and self.lexer_results[-1].family == "identifier":
                self.lexer_results = self.lexer.lex_states()

                self.endiamesos.genQuad('input', self.lexer_results[-1].recognized_string, '_', '_')
            else:
                print(f"ERROR: Δεν υπάρχει id, line {self.lexer_results[-1].line_number} στο {self.lexer_results[-1].recognized_string}")
                exit(-1)
    
    def call_stat(self):
       
        if not self.lexer_results:
            print("ERROR: No tokens available")
            exit(-1)

        if self.lexer_results[-1].family == "keyword" and self.lexer_results[-1].recognized_string == "εκτέλεσε":
            self.lexer_results = self.lexer.lex_states()
            if self.lexer_results and self.lexer_results[-1].family == "identifier":
                current_string = self.lexer_results[-1].recognized_string
                self.lexer_results = self.lexer.lex_states()
                self.idtail(current_string, 0)

                self.endiamesos.genQuad('call', current_string, '_',  '_')
            else:
                print(f"ERROR: Δεν υπάρχει id, line {self.lexer_results[-1].line_number} στο {self.lexer_results[-1].recognized_string}")
                exit(-1)
       


    def idtail(self, name, caller):
        if not self.lexer_results:
            print("ERROR: No tokens available")
            exit(-1)

        if self.lexer_results[-1].recognized_string == "(":
            self.actualpars()

            if (caller == 1):
                w = self.endiamesos.newTemp(self.pinakasSymvolwn)
                self.endiamesos.genQuad('par', w, 'RET', '_')
                self.endiamesos.genQuad('call', name, '_', '_')
                return w
        return name 
        
    def actualpars(self):
        if not self.lexer_results:
            print("ERROR: No tokens available")
            exit(-1)

        if self.lexer_results[-1].recognized_string == "(":
            self.lexer_results = self.lexer.lex_states()
            
            self.actualparlist()
            
            if self.lexer_results and self.lexer_results[-1].recognized_string == ")":
                self.lexer_results = self.lexer.lex_states()
            else:
                print(f"ERROR: Δεν κλείνει η ), line {self.lexer_results[-1].line_number} στο {self.lexer_results[-1].recognized_string}")
                exit(-1)
        
    def actualparlist(self):
        if not self.lexer_results:
            print("ERROR: No tokens available")
            exit(-1)

        self.actualparitem()

        while self.lexer_results and self.lexer_results[-1].recognized_string == ",":
            self.lexer_results = self.lexer.lex_states()
            self.actualparitem()    
    
    
    
    def actualparitem(self):
        if not self.lexer_results:
            print("ERROR: No tokens available")
            exit(-1)

        if self.lexer_results[-1].recognized_string == "%":
            self.lexer_results = self.lexer.lex_states()
            
            if self.lexer_results and self.lexer_results[-1].family == "identifier":
                current_string = self.lexer_results[-1].recognized_string
                self.lexer_results = self.lexer.lex_states()

                self.endiamesos.genQuad('par', current_string, 'REF', '_')
            else:
                print(f"ERROR: Perimenei kanonika onoma metavlitis meta to '%', line {self.lexer_results[-1].line_number}")
                exit(-1)
        else:
            E_place = self.expression()
            self.endiamesos.genQuad('par', E_place, 'CV', '_')
            
            
    def condition(self):
        bool_term1 = self.boolterm()

        current_true = bool_term1[0]
        current_false = bool_term1[1]
    
        while self.lexer_results and self.lexer_results[-1].recognized_string == "ή":
            self.lexer_results = self.lexer.lex_states()
            self.endiamesos.backPatch(current_false, self.endiamesos.nextQuad())
            
            bool_term2 = self.boolterm()

            current_true = self.endiamesos.merge(current_true, bool_term2[0])
            current_false = bool_term2[1]
        
        return current_true, current_false

    def boolterm(self):
        bool_factor1 = self.boolfactor()

        current_true = bool_factor1[0]
        current_false = bool_factor1[1]
        
        while self.lexer_results and self.lexer_results[-1].recognized_string == "και":
            self.lexer_results = self.lexer.lex_states()

            self.endiamesos.backPatch(current_true, self.endiamesos.nextQuad())
            
            bool_factor2 = self.boolfactor()

            current_false = self.endiamesos.merge(current_false, bool_factor2[1])
            current_true = bool_factor2[0]
        return current_true, current_false

    def boolfactor(self):
        if self.lexer_results and self.lexer_results[-1].recognized_string == "όχι":
            self.lexer_results = self.lexer.lex_states()
            
            if self.lexer_results and self.lexer_results[-1].recognized_string == "[":
                self.lexer_results = self.lexer.lex_states()
                condition = self.condition()

                current_true = condition[1]
                current_false = condition[0]
                
                if self.lexer_results and self.lexer_results[-1].recognized_string == "]":
                    self.lexer_results = self.lexer.lex_states()
                else:
                    print(f"ERROR: Δεν υπάρχει ] meta tin synthiki stin BOOLFACTOR, line {self.lexer_results[-1].line_number}")
                    exit(-1)
            else:
                print(f"ERROR: Θέλουμε [ meta to not stin BOOLFACTOR, line {self.lexer_results[-1].line_number}")
                exit(-1)

        elif self.lexer_results and self.lexer_results[-1].recognized_string == "[":
            self.lexer_results = self.lexer.lex_states()
            condition = self.condition()

            current_true  = condition[0]
            current_false = condition[1]
            
            if self.lexer_results and self.lexer_results[-1].recognized_string == "]":
                self.lexer_results = self.lexer.lex_states()
            else:
                print(f"ERROR: Δεν υπάρχει ] meta tin synthiki stin BOOLFACTOR, line {self.lexer_results[-1].line_number}")
                exit(-1)
        else:
            E_place1 = self.expression()
            relational_oper = self.relational_oper()
            E_place2 = self.expression()

            current_true = self.endiamesos.makeList(self.endiamesos.nextQuad())
            self.endiamesos.genQuad(relational_oper, E_place1, E_place2, '_')
            
            current_false = self.endiamesos.makeList(self.endiamesos.nextQuad())
            self.endiamesos.genQuad('jump', '_', '_', '_')
        return current_true, current_false

    def expression(self):
        optional_sign = self.optional_sign()
        T_1place = self.term()

        if ( optional_sign =='-' ):
            w = self.endiamesos.newTemp(self.pinakasSymvolwn)
            self.endiamesos.genQuad('-', '0', T_1place, w)
            T_1place = w


        while self.lexer_results and (self.lexer_results[-1].recognized_string == "+" or self.lexer_results[-1].recognized_string == "-"):
            add_Operation = self.add_oper()
            T_2place = self.term()

            #{P1}:
            w = self.endiamesos.newTemp(self.pinakasSymvolwn)
            self.endiamesos.genQuad(add_Operation, T_1place, T_2place, w)
            T_1place = w
        
        #{P2}:
        E_place = T_1place
        return E_place



    def term(self):
        F_1place = self.factor()
        
        while self.lexer_results and (self.lexer_results[-1].recognized_string == "*" or self.lexer_results[-1].recognized_string == "/"):
            mul_Operation = self.mul_oper()
            F_2place = self.factor()

            #{P1}:
            w = self.endiamesos.newTemp(self.pinakasSymvolwn)
            self.endiamesos.genQuad(mul_Operation, F_1place, F_2place, w)
            F_1place = w
        #{P2}:
        T_place =F_1place
        return T_place

    def factor(self):
        
        if not self.lexer_results:
            print("ERROR: No tokens available")
            exit(-1)

        if self.lexer_results[-1].family == "number":
            current_string = self.lexer_results[-1].recognized_string
            self.lexer_results = self.lexer.lex_states()

        elif self.lexer_results[-1].recognized_string == "(":
            self.lexer_results = self.lexer.lex_states()
            E_place = self.expression()
            current_string = E_place

            if self.lexer_results and self.lexer_results[-1].recognized_string == ")":
                self.lexer_results = self.lexer.lex_states()
            else:
                print(f"ERROR: Θέλουμε ) μετά το expression στη FACTOR, line {self.lexer_results[-1].line_number} στο {self.lexer_results[-1].recognized_string}")
                exit(-1)

        elif self.lexer_results[-1].family == "identifier":
            current_string_tmp = self.lexer_results[-1].recognized_string
            self.lexer_results = self.lexer.lex_states()
            current_string = self.idtail(current_string_tmp, 1)

        else:
            print(f"ERROR: Θέλουμε constant ή expression ή variable στην FACTOR, line {self.lexer_results[-1].line_number} στο {self.lexer_results[-1].recognized_string}")
            exit(-1)
        return current_string

    def relational_oper(self):
        print(f"[DEBUG] relational_oper: token = {self.lexer_results[-1]}")
        if self.lexer_results and self.lexer_results[-1].recognized_string == "=":
            current_string = self.lexer_results[-1].recognized_string
            self.lexer_results = self.lexer.lex_states()
        elif self.lexer_results and self.lexer_results[-1].recognized_string == "<":
            current_string = self.lexer_results[-1].recognized_string
            self.lexer_results = self.lexer.lex_states()
        elif self.lexer_results and self.lexer_results[-1].recognized_string == "<=":
            current_string = self.lexer_results[-1].recognized_string
            self.lexer_results = self.lexer.lex_states()
        elif self.lexer_results and self.lexer_results[-1].recognized_string == "<>":
            current_string = self.lexer_results[-1].recognized_string
            self.lexer_results = self.lexer.lex_states()
        elif self.lexer_results and self.lexer_results[-1].recognized_string == ">":
            current_string = self.lexer_results[-1].recognized_string
            self.lexer_results = self.lexer.lex_states()
        elif self.lexer_results and self.lexer_results[-1].recognized_string == ">=":
            current_string = self.lexer_results[-1].recognized_string
            self.lexer_results = self.lexer.lex_states()
        else:
            print(f"ERROR: Λείπει = or < or <= or <> or > or >=, line {self.lexer_results[-1].line_number} στο {self.lexer_results[-1].recognized_string}")
            exit(-1)
        return current_string

    def add_oper(self):
        if self.lexer_results and self.lexer_results[-1].recognized_string == "+":
            current_string = self.lexer_results[-1].recognized_string
            self.lexer_results = self.lexer.lex_states()
        elif self.lexer_results and self.lexer_results[-1].recognized_string == "-":
            current_string = self.lexer_results[-1].recognized_string
            self.lexer_results = self.lexer.lex_states()
        return current_string

    def mul_oper(self):
        if self.lexer_results and self.lexer_results[-1].recognized_string == "*":
            current_string = self.lexer_results[-1].recognized_string
            self.lexer_results = self.lexer.lex_states()
        elif self.lexer_results and self.lexer_results[-1].recognized_string == "/":
            current_string = self.lexer_results[-1].recognized_string
            self.lexer_results = self.lexer.lex_states()
        return current_string

    def optional_sign(self):
        if self.lexer_results and (self.lexer_results[-1].recognized_string == "+" or self.lexer_results[-1].recognized_string == "-"):
            add_oper = self.add_oper()
            return add_oper
        return '+'
    
    def intCode(self, x):
        lenQuads =  len(self.endiamesos.total_quads)
        for i in range(lenQuads):
            quad = self.endiamesos.total_quads[i]
            x.write(str(quad[0]))
            x.write(": ")
            x.write(str(quad[1]))
            x.write(", ")
            x.write(str(quad[2]))
            x.write(", ")
            x.write(str(quad[3]))
            x.write(", ")
            x.write(str(quad[4]))
            x.write("\n")
    def symTable(self, x):
        
        

        x.write("*" * 90 + "\n")
        x.write(f"Creating Symbol Table for {self.count} times\n")
        x.write("SYMBOL TABLE\n")

        for scope in reversed(self.pinakasSymvolwn.allSymbolsList):
            # Print scope details
            x.write(f"SCOPE: name: {scope.name} nestingLevel: {scope.nestingLevel}\n")
            x.write("\tENTITIES:\n")

            for entity in scope.entityList:
                # Print common entity details
                x.write(f"\tENTITY: name: {entity.name} type: {entity.entityType}")

                # Handle specific entity types
                if entity.entityType == 'VAR':
                    x.write(f" variable-type: {entity.variable.type} offset: {entity.variable.offset}")
                elif entity.entityType == 'TEMP':
                    x.write(f" temp-type: {entity.tmpvariable.type} offset: {entity.tmpvariable.offset}")
                elif entity.entityType == 'SUBPR':
                    x.write(f" subprogram-type: {entity.funcorproc.type} startQuad: {entity.funcorproc.startQuad} frameLength: {entity.funcorproc.frameLength}")
                    x.write("\n\t\tARGUMENTS:")
                    for argument in entity.funcorproc.arguments:
                       x.write(f"\n\t\tARGUMENT: name: {argument.name} type: {argument.type} parMode: {argument.parMode}")
                elif entity.entityType == 'PARAM':
                    x.write(f" mode: {entity.parameter.parMode} offset: {entity.parameter.offest}")

                x.write("\n")

            x.write("\n")

        x.write("*" * 90 + "\n\n")
        self.count += 1
        
    def final_code(self):


            for i in range(len(self.final.listOfAllQuads)):
                quad = self.final.listOfAllQuads[i]
                self.final.asc_file.write(f'L{quad[0]}: \n')

                op = quad[1]
                if op == 'jump':
                    self.final.asc_file.write(f'b L{quad[4]}\n')
                elif op == '=':
                    self.final.loadvr(quad[2], 1)
                    self.final.loadvr(quad[3], 2)
                    self.final.asc_file.write(f'beq t1,t2,L{quad[4]}\n')
                elif op == '<>':
                    self.final.loadvr(quad[2], 1)
                    self.final.loadvr(quad[3], 2)
                    self.final.asc_file.write(f'bne t1,t2,L{quad[4]}\n')
                elif op == '>':
                    self.final.loadvr(quad[2], 1)
                    self.final.loadvr(quad[3], 2)
                    self.final.asc_file.write(f'bgt t1,t2,L{quad[4]}\n')
                elif op == '<':
                    self.final.loadvr(quad[2], 1)
                    self.final.loadvr(quad[3], 2)
                    self.final.asc_file.write(f'blt t1,t2,L{quad[4]}\n')
                elif op == '>=':
                    self.final.loadvr(quad[2], 1)
                    self.final.loadvr(quad[3], 2)
                    self.final.asc_file.write(f'bge t1,t2,L{quad[4]}\n')
                elif op == '<=':
                    self.final.loadvr(quad[2], 1)
                    self.final.loadvr(quad[3], 2)
                    self.final.asc_file.write(f'ble t1,t2,L{quad[4]}\n')
                elif op == ':=':
                    self.final.loadvr(quad[2], 1)
                    self.final.storerv(1, quad[4])
                elif op == '+':
                    self.final.loadvr(quad[2], 1)
                    self.final.loadvr(quad[3], 2)
                    self.final.asc_file.write('add t1,t1,t2\n')
                    self.final.storerv(1, quad[4])
                elif op == '-':
                    self.final.loadvr(quad[2], 1)
                    self.final.loadvr(quad[3], 2)
                    self.final.asc_file.write('sub t1,t1,t2\n')
                    self.final.storerv(1, quad[4])
                elif op == '*':
                    self.final.loadvr(quad[2], 1)
                    self.final.loadvr(quad[3], 2)
                    self.final.asc_file.write('mul t1,t1,t2\n')
                    self.final.storerv(1, quad[4])
                elif op == '/':
                    self.final.loadvr(quad[2], 1)
                    self.final.loadvr(quad[3], 2)
                    self.final.asc_file.write('div t1,t1,t2\n')
                    self.final.storerv(1, quad[4])
                elif op == 'out':
                    self.final.loadvr(quad[2], 1)
                    self.final.asc_file.write('mv a0,t1\n')
                    self.final.asc_file.write('li a7,1\n')
                    self.final.asc_file.write('ecall\n')
                elif op == 'input' or op == 'inp':
                    self.final.asc_file.write('li a7,5\n')
                    self.final.asc_file.write('ecall\n')
                    self.final.asc_file.write('mv t1,a0\n')
                    self.final.storerv(1, quad[2])
                elif op == 'par':
                    if self.seira == -1:
                        fname = self.final.search_list_for_call(i)
                        if self.final.is_valid_identifier(fname):
                            sc1, ent1 = self.final.search_entity(fname)
                            self.final.asc_file.write(f'addi fp,sp,{ent1.funcorproc.frameLength}\n')
                        self.seira = 0
                    if quad[3] == 'CV':
                        if self.final.is_constant(quad[2]):
                            self.final.asc_file.write(f'li t0,{quad[2]}\n')
                        else:
                            self.final.loadvr(quad[2], 0)
                        self.final.asc_file.write(f'sw t0,-{12+4*self.seira}(fp)\n')
                        self.seira += 1
                    elif quad[3] == 'RET':
                        #print(f"[DEBUG] Calling search_entity with argument: {quad[2]}")
                        if not self.final.is_constant(quad[2]) and self.final.is_valid_identifier(quad[2]):
                            sc1, ent1 = self.final.search_entity(quad[2])
                            self.final.asc_file.write(f'addi t0,sp,-{ent1.tmpvariable.offset}\n')
                            self.final.asc_file.write('sw t0,-8(fp)\n')
                    elif quad[3] == 'REF':
                        if not self.final.is_constant(quad[2]) and self.final.is_valid_identifier(quad[2]):
                            sc1, ent1 = self.final.search_entity(quad[2])
                            if sc1.nestingLevel == self.final.scopesList[-1].nestingLevel:
                                if ent1.entityType == 'VAR':
                                    self.final.asc_file.write(f'addi t0,sp,-{ent1.variable.offset}\n')
                                    self.final.asc_file.write(f'sw t0,-{12+4*self.seira}(fp)\n')
                                elif ent1.entityType == 'PARAM' and ent1.parameter.mode == 'CV':
                                    self.final.asc_file.write(f'addi t0,sp,-{ent1.parameter.offset}\n')
                                    self.final.asc_file.write(f'sw t0,-{12+4*self.seira}(fp)\n')
                                elif ent1.entityType == 'PARAM' and ent1.parameter.mode == 'REF':
                                    self.final.asc_file.write(f'lw t0,-{ent1.parameter.offset}(sp)\n')
                                    self.final.asc_file.write(f'sw t0,-{12+4*self.seira}(fp)\n')
                            elif sc1.nestingLevel < self.final.scopesList[-1].nestingLevel:
                                if ent1.entityType == 'PARAM' and ent1.parameter.mode == 'REF':
                                    self.gnlvcode(quad[2])
                                    self.final.asc_file.write('lw t0,(t0)\n')
                                    self.final.asc_file.write(f'sw t0,-{12+4*self.seira}(fp)\n')
                                else:
                                    self.gnlvcode(quad[2])
                                    self.final.asc_file.write(f'sw t0,-{12+4*self.seira}(fp)\n')
                            self.seira += 1
                elif op == 'call':
                    self.seira = -1
                    if self.final.is_valid_identifier(quad[2]):
                        sc1, ent1 = self.final.search_entity(quad[2])
                        if self.final.scopesList[-1].nestingLevel == sc1.nestingLevel:
                            self.final.asc_file.write('lw t0,-4(sp)\n')
                            self.final.asc_file.write('sw t0,-4(fp)\n')
                        elif self.final.scopesList[-1].nestingLevel < sc1.nestingLevel:
                            self.final.asc_file.write('sw sp,-4(fp)\n')
                        self.final.asc_file.write(f'addi sp,sp,{ent1.funcorproc.frameLength}\n')
                        self.final.asc_file.write(f'jal L{ent1.funcorproc.startQuad}\n')
                        self.final.asc_file.write(f'addi sp,sp,-{ent1.funcorproc.frameLength}\n')
                elif op == 'begin_block' and self.final.scopesList[-1].nestingLevel != 0:
                    self.final.asc_file.write('sw ra,(sp)\n')
                elif op == 'begin_block' and self.final.scopesList[-1].nestingLevel == 0:
                    self.final.asc_file.seek(0, os.SEEK_SET)
                    self.final.asc_file.write(f'j L{quad[0]}\n')
                    self.final.asc_file.seek(0, os.SEEK_END)
                    # Υπολόγισε το offset με βάση το τρέχον scope
                    offset = 0
                    if self.final.scopesList:
                        offset = 12 + 4 * sum(1 for ent in self.final.scopesList[-1].entityList if ent.entityType in ('VAR', 'TEMP', 'PARAM'))
                    self.final.asc_file.write(f'addi sp,sp,{offset}\n')
                    self.final.asc_file.write('mv gp,sp\n')
                elif op == 'end_block' and self.final.scopesList[-1].nestingLevel != 0:
                    self.final.asc_file.write('lw ra,(sp)\n')
                    self.final.asc_file.write('jr ra\n')
                elif op == 'halt':
                    self.final.asc_file.write('li a0,0\n')
                    self.final.asc_file.write('li a7,93\n')
                    self.final.asc_file.write('ecall\n')

            # Καθάρισε τις τετράδες για το επόμενο scope/block
            self.final.listOfAllQuads.clear()
    


class Final():
    
    #asc_file = open('asc_file.asm','w') 
    #asc_file.write('         \n\n\n') # afino keno wste na mpei to "j Lmain"
    
    def __init__(self, scopesList, listOfAllQuads, asc_file):
        self.scopesList = scopesList
        self.listOfAllQuads = listOfAllQuads
        self.asc_file = asc_file
        asc_file.write('         \n\n\n') #
        
    
    def search_entity(self, n):
        n = str(n) # Always treat n as a string
        #print(f"[DEBUG] search_entity called with n={n} (type: {type(n)})")
        for sco in reversed(self.scopesList):
            for ent in sco.entityList:
                if ent.name == n:
                    #print(f"[DEBUG] Entity found: {ent.name} (type: {ent.entityType}) in scope {sco.name}")
                    return (sco, ent)
        print("Den brethike ston pinaka simbolon entity me onoma " + str(n))
        exit(-1)
        
    def gnlvcode(self, name):
        if not self.is_valid_identifier(name):
            #print(f"[DEBUG] gnlvcode: Skipping non-identifier: {name}")
            return
        self.asc_file.write('lw t0,-4(sp)\n')
        sc1, ent1 = self.search_entity(name)
        my_help = self.scopesList[-1].nestingLevel - sc1.nestingLevel - 1
        for _ in range(my_help):
            self.asc_file.write('lw t0,-4(t0)\n')
        if ent1.entityType == 'VAR':
            x = ent1.variable.offset
        elif ent1.entityType == 'PARAM':
            x = ent1.parameter.offset
        self.asc_file.write(f'addi t0,t0,-{x}\n')

    def loadvr(self, v, r):  #DIAFANEIES 26 eos 32 (r akeraios, v string)
        
        if v.isdigit():
            self.asc_file.write(f'li t{r},{v}\n')
            
        elif self.is_valid_identifier(v):
            
            sc1, ent1 = self.search_entity(v)

            #DIAFANEIA 26
            if sc1.nestingLevel == 0 and ent1.entityType == 'VAR':
                self.asc_file.write(f'lw t{r},-{ent1.variable.offset}(gp)\n')

            elif sc1.nestingLevel == self.scopesList[-1].nestingLevel:

                if ent1.entityType == 'TEMP':
                    self.asc_file.write(f'lw t{r},-{ent1.tmpvariable.offset}(sp)\n')
                elif ent1.entityType == 'VAR':
                    self.asc_file.write(f'lw t{r},-{ent1.variable.offset}(sp)\n')

                elif ent1.entityType == 'PARAM' and ent1.parameter.parMode == 'CV':
                    self.asc_file.write(f'lw t{r},-{ent1.parameter.offset}(sp)\n')
                elif ent1.entityType == 'PARAM' and ent1.parameter.parMode == 'REF':
                    self.asc_file.write(f'lw t0,-{ent1.parameter.offset}(sp)\n')
                    self.asc_file.write(f'lw t{r},(t0)\n')
                    
            elif sc1.nestingLevel < self.scopesList[-1].nestingLevel:

                if ent1.entityType == 'VAR' or (ent1.entityType == 'PARAM' and ent1.parameter.parMode == 'CV'):
                    self.gnlvcode(v)
                    self.asc_file.write(f'lw t{r},(t0)\n')

                elif ent1.entityType == 'PARAM' and ent1.parameter.parMode == 'REF':
                    self.gnlvcode(v)
                    self.asc_file.write('lw t0,(t0)\n')
                    self.asc_file.write(f'lw t{r},(t0)\n')
    
    def storerv(self, r, v):
        
        if self.is_constant(v):
            # You probably don't want to store to a constant, so just return or raise an error
            #print(f"[DEBUG] storerv called with constant {v}, skipping store.")
            return

        if not self.is_valid_identifier(v):
            #print(f"[DEBUG] storerv: Skipping non-identifier: {v}")
            return
        
        sc1, ent1 = self.search_entity(v)
        
        if sc1.nestingLevel == 0 and ent1.entityType == 'VAR':
            self.asc_file.write(f'sw t{r},-{ent1.variable.offset}(gp)\n')
            
        elif sc1.nestingLevel == self.scopesList[-1].nestingLevel:

            if ent1.entityType == 'VAR':
                self.asc_file.write(f'sw t{r},-{ent1.variable.offset}(sp)\n')
            elif ent1.entityType == 'TEMP':
                self.asc_file.write(f'sw t{r},-{ent1.tmpvariable.offset}(sp)\n')
            elif ent1.entityType == 'PARAM' and ent1.parameter.parMode == 'CV':
                self.asc_file.write(f'sw t{r},-{ent1.parameter.offset}(sp)\n')
            elif ent1.entityType == 'PARAM' and ent1.parameter.parMode == 'REF':
                self.asc_file.write(f'lw t0,-{ent1.parameter.offset}(sp)\n')
                self.asc_file.write(f'sw t{r},(t0)\n')
                
        elif sc1.nestingLevel < self.scopesList[-1].nestingLevel:

            if ent1.entityType == 'VAR' or (ent1.entityType == 'PARAM' and ent1.parameter.parMode == 'CV'):
                self.gnlvcode(v)
                self.asc_file.write(f'sw t{r},(t0)\n')
            elif ent1.entityType == 'PARAM' and ent1.parameter.parMode == 'REF':
                self.gnlvcode(v)
                self.asc_file.write('lw t0,(t0)\n')
                self.asc_file.write(f'sw t{r},(t0)\n')
            #DIAFANEIA 35 (katw) αν v είναι τυπική παράμετρος που περνάει με αναφορά
            elif ent1.entityType == 'SUBPR' and ent1.funcorproc.type == 'Function':
                self.asc_file.write('lw t0,-8(sp)\n')
                self.asc_file.write(f'sw t{r},(t0)\n')
                
                
    def search_list_for_call(self, i):
        """
        Ψάχνει να βρει το 'call' ξεκινώντας από το i και προς τα εμπρός.
        Επιστρέφει το όνομα του υποπρογράμματος που καλείται.
        """
        start = i
        while start < len(self.listOfAllQuads):
            if self.listOfAllQuads[start][1] == 'call':
                return str(self.listOfAllQuads[start][2])
            start += 1
        return None  # Αν δεν βρεθεί, επιστρέφει None
    
    
    def is_constant(self, v):
        try:
            int(v)
            return True
        except ValueError:
            return False
        
    def is_valid_identifier(self, v):
        # Επιστρέφει True αν το v είναι έγκυρο όνομα μεταβλητής (identifier)
        # και δεν είναι αριθμός (constant)
        return v.isidentifier() and not self.is_constant(v)
    
    
        


    
    
    


file_path = input("Δώσε το όνομα του αρχείου για ανάλυση: ")
syntax = Syntaktikos(1, file_path, '')



