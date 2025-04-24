# DIMITRIOS PAGONIS 4985
# DIMITRIOS TZALOKOSTAS 4994


import string
import sys
import argparse

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
                    self.readen_string += chr
                    next_state = self.relationalOperator_token
                    self.index += 1
                    return self.resetStartState(self.readen_string, next_state, self.current_line)
                    #continue
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

class EndiamesosKwdikas:
    
    def __init__(self):
        self.total_quads = []
        self.count = 1
        self.T_i = 1
    
    def next_quad(self):
        
        return self.count
    
    def genQuad(self, one, two, three, four):
        quad = [self.next_quad(), one, two, three, four] #dhmioyrgia 4adas
        self.total_quads.append(quad)
        self.count += 1
        return quad
    
    def newTemp(self):
        
        tmp = "T_"+ str(self.T_i)
        self.T_i +=1

        return tmp
    
    def emptyList(self):
        
        return []
    
    def makeList(self, x):
        
        return [x]

    def merge(self, i, j):

        return (i + j)

    def backpatch(self, l, label_target):
        # to l einai lista me deiktes pou deixnoyn poia quads den einai symplhrwmena 

        length_l = len(l)
        length_totalQuads = len(self.total_quads)

        for i in length_l:
            for j in length_totalQuads:
                if(list[i] == self.total_quads[j][0] and self.total_quads[j][-1] == '_'):
                    self.total_quads[j][-1] = label_target
                    break
        return
                  

class Syntaktikos:
    def __init__(self, line_number, file_path, token):
        self.line_number = line_number
        self.file_path = file_path
        self.token = token
        self.lexer = Lex(line_number, file_path, token)
        self.lexer_results = []
        self.program()
        

    def program(self):
        self.lexer_results = self.lexer.lex_states()
        if not self.lexer_results:
            print("ERROR: No tokens found")
            exit(-1)

        if self.lexer_results[-1].family == "keyword" and self.lexer_results[-1].recognized_string == "πρόγραμμα":
            self.lexer_results = self.lexer.lex_states()
            if self.lexer_results and self.lexer_results[-1].family == "identifier":
                self.lexer_results = self.lexer.lex_states()
                self.programblock()
                
            else:
                print(f"ERROR: Δεν υπάρχει onoma programmatos, line {self.lexer_results[-1].line_number}")
                exit(-1)
        else:
            print(f"ERROR: H leksi 'πρόγραμμα' Δεν υπάρχει stin arxi tou programmatos, line {self.lexer_results[-1].line_number}")
            exit(-1)


    def programblock(self):
        self.declarations()
        self.subprograms()
        #self.lexer_results = self.lexer.lex_states()
       

        if self.lexer_results and self.lexer_results[-1].family == "keyword" and self.lexer_results[-1].recognized_string == "αρχή_προγράμματος":
            self.lexer_results = self.lexer.lex_states()
            
            self.sequence()

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
            self.varlist()
            
    def varlist(self):
       
        if self.lexer_results and self.lexer_results[-1].family == "identifier":
            self.lexer_results = self.lexer.lex_states()
            while self.lexer_results and self.lexer_results[-1].family == "delimeter" and self.lexer_results[-1].recognized_string == ',':
                self.lexer_results = self.lexer.lex_states()
                if self.lexer_results and self.lexer_results[-1].family == "identifier":
                    self.lexer_results = self.lexer.lex_states()
                else:
                    print(f"ERROR: Δεν υπάρχει onoma metablitis, line {self.lexer_results[-1].line_number}")
                    exit(-1)
        else:
            print(f"ERROR: Δεν υπάρχει onoma metablitis, line {self.lexer_results[-1].line_number}")
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
                self.lexer_results = self.lexer.lex_states()
                
                if self.lexer_results and self.lexer_results[-1].recognized_string == '(':
                    self.lexer_results = self.lexer.lex_states()
                    self.formalparlist()

                    if self.lexer_results and self.lexer_results[-1].recognized_string == ')':
                        self.lexer_results = self.lexer.lex_states()
                        self.funcblock()
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
                self.lexer_results = self.lexer.lex_states()
                if self.lexer_results and self.lexer_results[-1].recognized_string == '(':
                    self.lexer_results = self.lexer.lex_states()
                    self.formalparlist()
                    if self.lexer_results and self.lexer_results[-1].recognized_string == ')':
                        self.lexer_results = self.lexer.lex_states()
                        self.procblock()
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
            self.varlist()
        else:
            print(f"ERROR: Δεν υπάρχει id sti formalparlist, line {self.lexer_results[-1].line_number}")
            exit(-1)

    def funcblock(self):
        
        if self.lexer_results and self.lexer_results[-1].family == "keyword" and self.lexer_results[-1].recognized_string == "διαπροσωπεία":
            self.lexer_results = self.lexer.lex_states()
            self.funcinput()
            self.funcoutput()
            self.declarations()
            if self.lexer_results and self.lexer_results[-1].family == "keyword" and self.lexer_results[-1].recognized_string == "αρχή_συνάρτησης":
                self.lexer_results = self.lexer.lex_states()
                self.sequence()
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

    
    
    
    def procblock(self):
        if self.lexer_results and self.lexer_results[-1].family == "keyword" and self.lexer_results[-1].recognized_string == "διαπροσωπεία":
            self.lexer_results = self.lexer.lex_states()
            self.funcinput()
            self.funcoutput()
            self.declarations()
            if self.lexer_results and self.lexer_results[-1].family == "keyword" and self.lexer_results[-1].recognized_string == "αρχή_διαδικασίας":
                self.lexer_results = self.lexer.lex_states()
                self.sequence()
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
            self.varlist()


    def funcoutput(self):
        
        if self.lexer_results[-1].family == "keyword" and self.lexer_results[-1].recognized_string == "έξοδος":
            self.lexer_results = self.lexer.lex_states()
            self.varlist()

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
            self.lexer_results = self.lexer.lex_states()
            
            if self.lexer_results and self.lexer_results[-1].recognized_string == ":=":
                self.lexer_results = self.lexer.lex_states()
                self.expression()
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
            self.condition()

            if self.lexer_results and self.lexer_results[-1].recognized_string == "τότε":
                self.lexer_results = self.lexer.lex_states()
                self.sequence()
                self.elsepart()
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
            self.condition()

            if self.lexer_results and self.lexer_results[-1].recognized_string == "επανάλαβε":
                self.lexer_results = self.lexer.lex_states()
                self.sequence()

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
            self.sequence()

            if self.lexer_results and self.lexer_results[-1].recognized_string == "μέχρι":
                self.lexer_results = self.lexer.lex_states()

                self.condition()
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
                self.lexer_results = self.lexer.lex_states()
                if self.lexer_results and self.lexer_results[-1].recognized_string == ":=":
                    self.lexer_results = self.lexer.lex_states()
                    self.expression()
                    if self.lexer_results and self.lexer_results[-1].recognized_string == "έως":
                        self.lexer_results = self.lexer.lex_states()
                        self.expression()
                        if self.lexer_results and self.lexer_results[-1].recognized_string == "με_βήμα":
                            self.step()
                            if self.lexer_results and self.lexer_results[-1].recognized_string == "επανάλαβε":
                                self.lexer_results = self.lexer.lex_states()
                                self.sequence()
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
            self.expression()
       

    
    def print_stat(self):
       
        if not self.lexer_results:
            print("ERROR: No tokens available")
            exit(-1)

        if self.lexer_results[-1].family == "keyword" and self.lexer_results[-1].recognized_string == "γράψε":
            self.lexer_results = self.lexer.lex_states()
            self.expression()
        
    def input_stat(self):
       
        if not self.lexer_results:
            print("ERROR: No tokens available")
            exit(-1)

        if self.lexer_results[-1].family == "keyword" and self.lexer_results[-1].recognized_string == "διάβασε":
            self.lexer_results = self.lexer.lex_states()
            if self.lexer_results and self.lexer_results[-1].family == "identifier":
                self.lexer_results = self.lexer.lex_states()
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
                self.lexer_results = self.lexer.lex_states()
                self.idtail()
            else:
                print(f"ERROR: Δεν υπάρχει id, line {self.lexer_results[-1].line_number} στο {self.lexer_results[-1].recognized_string}")
                exit(-1)
       


    def idtail(self):
        if not self.lexer_results:
            print("ERROR: No tokens available")
            exit(-1)

        if self.lexer_results[-1].recognized_string == "(":
            self.actualpars()
        
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
                self.lexer_results = self.lexer.lex_states()
            else:
                print(f"ERROR: Perimenei kanonika onoma metavlitis meta to '%', line {self.lexer_results[-1].line_number}")
                exit(-1)
        else:
            self.expression()
            
            
    def condition(self):
        self.boolterm()
    
        while self.lexer_results and self.lexer_results[-1].recognized_string == "ή":
            self.lexer_results = self.lexer.lex_states()
            self.boolterm()

    def boolterm(self):
        self.boolfactor()
        
        while self.lexer_results and self.lexer_results[-1].recognized_string == "και":
            self.lexer_results = self.lexer.lex_states()
            self.boolfactor()

    def boolfactor(self):
        if self.lexer_results and self.lexer_results[-1].recognized_string == "όχι":
            self.lexer_results = self.lexer.lex_states()
            
            if self.lexer_results and self.lexer_results[-1].recognized_string == "[":
                self.lexer_results = self.lexer.lex_states()
                self.condition()
                
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
            self.condition()
            
            if self.lexer_results and self.lexer_results[-1].recognized_string == "]":
                self.lexer_results = self.lexer.lex_states()
            else:
                print(f"ERROR: Δεν υπάρχει ] meta tin synthiki stin BOOLFACTOR, line {self.lexer_results[-1].line_number}")
                exit(-1)
        else:
            self.expression()
            self.relational_oper()
            self.expression()

    def expression(self):
        self.optional_sign()
        self.term()

        while self.lexer_results and (self.lexer_results[-1].recognized_string == "+" or self.lexer_results[-1].recognized_string == "-"):
            self.add_oper()
            self.term()

    def term(self):
        self.factor()
        
        while self.lexer_results and (self.lexer_results[-1].recognized_string == "*" or self.lexer_results[-1].recognized_string == "/"):
            self.mul_oper()
            self.factor()

    def factor(self):
        
        if not self.lexer_results:
            print("ERROR: No tokens available")
            exit(-1)

        if self.lexer_results[-1].family == "number":
            self.lexer_results = self.lexer.lex_states()

        elif self.lexer_results[-1].recognized_string == "(":
            self.lexer_results = self.lexer.lex_states()
            self.expression()

            if self.lexer_results and self.lexer_results[-1].recognized_string == ")":
                self.lexer_results = self.lexer.lex_states()
            else:
                print(f"ERROR: Θέλουμε ) μετά το expression στη FACTOR, line {self.lexer_results[-1].line_number} στο {self.lexer_results[-1].recognized_string}")
                exit(-1)

        elif self.lexer_results[-1].family == "identifier":
            self.lexer_results = self.lexer.lex_states()
            self.idtail()

        else:
            print(f"ERROR: Θέλουμε constant h expression h variable stin FACTOR, line {self.lexer_results[-1].line_number} στο {self.lexer_results[-1].recognized_string}")
            exit(-1)

    def relational_oper(self):
        if self.lexer_results and self.lexer_results[-1].recognized_string == ":=":
            self.lexer_results = self.lexer.lex_states()
        elif self.lexer_results and self.lexer_results[-1].recognized_string == "<":
            self.lexer_results = self.lexer.lex_states()
        elif self.lexer_results and self.lexer_results[-1].recognized_string == "<=":
            self.lexer_results = self.lexer.lex_states()
        elif self.lexer_results and self.lexer_results[-1].recognized_string == "<>":
            self.lexer_results = self.lexer.lex_states()
        elif self.lexer_results and self.lexer_results[-1].recognized_string == ">":
            self.lexer_results = self.lexer.lex_states()
        elif self.lexer_results and self.lexer_results[-1].recognized_string == ">=":
            self.lexer_results = self.lexer.lex_states()
        else:
            print(f"ERROR: Λείπει := or < or <= or <> or > or >=, line {self.lexer_results[-1].line_number} στο {self.lexer_results[-1].recognized_string}")
            exit(-1)

    def add_oper(self):
        if self.lexer_results and self.lexer_results[-1].recognized_string == "+":
            self.lexer_results = self.lexer.lex_states()
        elif self.lexer_results and self.lexer_results[-1].recognized_string == "-":
            self.lexer_results = self.lexer.lex_states()

    def mul_oper(self):
        if self.lexer_results and self.lexer_results[-1].recognized_string == "*":
            self.lexer_results = self.lexer.lex_states()
        elif self.lexer_results and self.lexer_results[-1].recognized_string == "/":
            self.lexer_results = self.lexer.lex_states()

    def optional_sign(self):
        if self.lexer_results and (self.lexer_results[-1].recognized_string == "+" or self.lexer_results[-1].recognized_string == "-"):
            self.add_oper()
            


file_path = input("Δώσε το όνομα του αρχείου για ανάλυση: ")
syntax = Syntaktikos(1, file_path, '')