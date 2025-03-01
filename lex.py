# DIMITRIOS PAGONIS 4985
# DIMITRIOS TZALOKOSTAS 4994
##22

import string
import sys
import argparse

class Token:
    def __init__(self, recognized_string, family, line_number):
        self.recognized_string = recognized_string
        self.family = family
        self.line_number = line_number
    
    def __str__(self):
        return f"String: {self.recognized_string}, Family: {self.family}, Line: {self.line_number}"

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
        self.lex_states()
   
    def read_file_content(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
  
    def __del__(self):
        pass

    def error(self, readen_string, current_line):
        print(f"Lexical error at line {self.current_line}: {self.readen_string}")
        self.readen_string = self.readen_string[:-1]
        #self.index -= 1
        self.state = self.start_state
        
    
    def next_token(self, readen_string, next_state, line_number):
        # return Token object
        if self.check_keyword(self.readen_string):
            next_state = self.keyword_token

        token_family = self.tokens[next_state]
        token = Token(self.readen_string, token_family, line_number)
        print(token)

        return token

    def check_keyword(self, string):
        if string in self.keywords:
            return True
        return False
    def resetStartState(self, readen_string,next_state, line_number):
        self.next_token(self.readen_string, next_state, self.current_line)
        self.readen_string = ''
        self.state = self.start_state
        
        
        

  
    def lex_states(self):
        self.state = self.start_state
        next_state = ''
        
        try:
            while self.index < len(self.content):
                chr = self.content[self.index]
                if self.state == self.start_state:
                    if chr.isspace():
                        next_state = self.start_state
                        if chr == '\n':
                            self.current_line += 1
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
                        self.index += 1
                        if chr == '\n':
                            self.current_line += 1
                        
                        self.state = next_state
                        next_state = ''
                        continue
                    

                    elif chr == '_':
                        self.readen_string += chr
                        self.error(self.readen_string, self.current_line)
                        continue
                    

                    elif chr not in self.valid_characters:
                        self.readen_string += chr
                        self.error(self.readen_string, self.current_line)
                        self.index += 1
                        continue

                    if next_state != self.start_state or next_state != self.rem_state:
                        self.readen_string += chr
                    
                
                elif self.state == self.dig_state:
                    if chr.isdigit():
                        self.readen_string += chr
                        next_state = self.dig_state
                    elif chr.isalpha():
                        self.error()
                    else:
                        next_state = self.number_token
                        self.resetStartState(self.readen_string, next_state, self.current_line)
                        continue
                elif self.state == self.idk_state:
                    if chr.isalpha() or chr.isdigit() or chr == '_':
                        self.readen_string += chr
                        
                        next_state = self.idk_state
                    else:
                        next_state = self.identifier_token
                        self.resetStartState(self.readen_string, next_state, self.current_line)
                        continue

                elif self.state == self.addOperator_token:
                    
                    next_state = self.addOperator_token
                    self.resetStartState(self.readen_string, next_state, self.current_line)
                    continue

                elif self.state == self.mulOperator_token:
                    
                    next_state = self.mulOperator_token
                    self.resetStartState(self.readen_string, next_state, self.current_line)
                    continue

                elif self.state == self.delimeter_token:
                    
                    next_state = self.delimeter_token
                    self.resetStartState(self.readen_string, next_state, self.current_line)
                    continue

                elif self.state == self.groupSymbols_token:
                    
                    next_state = self.groupSymbols_token
                    self.resetStartState(self.readen_string, next_state, self.current_line)
                    continue
                elif self.state == self.lessthan_state:
                    self.readen_string += chr
                    if self.readen_string in self.multiTokens:
                        next_state = self.relationalOperator_token
                        self.resetStartState(self.readen_string, next_state, self.current_line)
                        self.index += 1
                        continue
                
                    else:
                        self.error()

                elif self.state == self.greaterthan_state:
                    self.readen_string += chr
                    if self.readen_string in self.multiTokens:
                        next_state = self.relationalOperator_token
                        self.resetStartState(self.readen_string, next_state, self.current_line)
                        self.index += 1
                        continue
                    else:
                        self.error()

                elif self.state == self.relationalOperator_token:
                    self.readen_string += chr
                    next_state = self.relationalOperator_token
                    self.resetStartState(self.readen_string, next_state, self.current_line)
                    self.index += 1
                    continue
                elif self.state == self.asgn_state:
                    self.readen_string += chr
                    if self.readen_string in self.multiTokens:
                        next_state = self.assignent_token
                        self.resetStartState(self.readen_string, next_state, self.current_line)
                        self.index += 1
                        continue
                    else: #error
                        self.error(self.readen_string, self.current_line)
                        continue
                elif self.state == self.rem_state:
                    if chr == '}':
                        next_state = self.start_state
                        
                    else:
                        next_state = self.rem_state
                    if chr == '\n':
                        self.current_line += 1
                
                
                self.index += 1
                self.state = next_state
                next_state = ''
            if  self.index >= len(self.content):
                print("eof reached")
        except Exception as e:
            print(e)
       
            

if __name__ == "__main__":
    file_path = input("Δώσε το όνομα του αρχείου για ανάλυση: ")
    lex = Lex(1, file_path, '')

