import os
import sys

alphabet =['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q',
'R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k',
'l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
'Α','Β','Γ','Δ','Ε','Ζ','Η','Θ','Ι','Κ','Λ','Μ','Ν','Ξ','Ο','Π','Ρ','Σ','Τ','Υ','Φ','Χ','Ψ','Ω',
'Ά','Έ','Ή','Ί','Ό','Ύ','Ώ',
'α','β','γ','δ','ε','ζ','η','θ','ι','κ','λ','μ','ν','ξ','ο','π','ρ','σ','τ','υ','φ','χ','ψ','ω','ς',
'ά','έ','ή','ί','ό','ύ','ώ']
numbers=['0','1','2','3','4','5','6','7','8','9']

file= open('final_check.gre','r',encoding='utf-8')


#Xaraktires pinaka metavasewn

white_char=0 # to space(keno) h' to tab
letters=1 # oloi oi ellinikoi kai agglikoi xaraktires
num=2  # ola ta psifia (0 ews 9)
plus=3 # +
minus=4 # -
multiply=5 # *
divide=6 #  /
modulo=7 #  %
equal=8 # =
less_than=9 # <
greater_than=10 # >
EOF=11 # den einai ektiposimos, einai PANTA o teleutaios xaraktiras tou arxeiou
oxi_apodekto_simvolo=12 # opoiodipote simvolo pou DEN einai ta ypoloipa
koma=13 # ,
arist_parenthesi=14 # (
deksia_parenthesi=15 # )
arist_aggili=16 # [
deksia_aggili=17 # ]
anoigma_block=18 # {
kleisimo_block=19 # }
allagi_grammis= 20 
anwkatw_teleia= 21 # :
katw_paula=22 # _
erotimatiko=23 # ;


#Katastaseis

katastasi_start=0
katastasi_letter=1
katastasi_num=2
katastasi_lessthan=3
katastasi_greaterthan=4
katastasi_anwkatwteleia=5
katastasi_sxolia=6


#Tokens

id_tk=30   # identifiers
num_tk=31   # number
plus_tk=32
minus_tk=33
multiply_tk=34
divide_tk=35
modulo_tk=36
equal_tk=37
lessthan_tk=38
greaterthan_tk=39
EOF_tk=40
koma_tk=41
arist_parenthesi_tk=42
deksia_parenthesi_tk=43
arist_aggili_tk=44
deksia_aggili_tk=45
anoigma_block_tk=46 # {
kleisimo_block_tk=47 # }
lessORequal_tk=48 # <=
greaterORequal_tk=49 # >=
anwkatw_teleia_tk=50
anathesi_tk=51 # :=
diaforo_tk=52 # <>
erotimatiko_tk=53 # ;


# Desmeumenes lekseis
program_tk=100
declare_tk=101
if_tk=102
then_tk=103
else_tk=104
endif_tk=105
repeat_tk=106
until_tk=107
while_tk=108
endwhile_tk=109
for_tk=110
to_tk=111
step_tk=112
endfor_tk=113
print_tk=114
input_tk=115
and_tk=116
or_tk=117
not_tk=118
function_tk=119
procedure_tk=120
interface_tk=121
in_tk=122
inout_tk=123
beginfunction_tk=124
endfunction_tk=125
beginprocedure_tk=126
endprocedure_tk=127
beginprogram_tk=128
endprogram_tk=129
call_tk=130



#Errors (mporoun na ginoun kai thetika)

ERROR_MH_APODEKTO_SYMBOLO=-1
ERROR_PSIFIO_GRAMMA=-2
ERROR_PANW_APO_30_CHARAKTIRES=-3
ERROR_ANOIGMA_SXOLIWN_ME_EOF=-4
ERROR_DEKSI_AGGISTRO_MONO_TOU=-5
ERROR_KATW_PAYLA_MONI_TIS=-6

pinakas_metavasewn=[
    #katastasi_start
        [katastasi_start,katastasi_letter,katastasi_num,plus_tk,minus_tk,multiply_tk, divide_tk, modulo_tk,
         equal_tk,katastasi_lessthan,katastasi_greaterthan,EOF_tk,ERROR_MH_APODEKTO_SYMBOLO, koma_tk, 
         arist_parenthesi_tk,deksia_parenthesi_tk,arist_aggili_tk,deksia_aggili_tk,katastasi_sxolia,
         ERROR_DEKSI_AGGISTRO_MONO_TOU,katastasi_start,katastasi_anwkatwteleia,ERROR_KATW_PAYLA_MONI_TIS,erotimatiko_tk],

    #katastasi_letter
        [id_tk,katastasi_letter,katastasi_letter,id_tk,id_tk,id_tk,id_tk,id_tk,id_tk,id_tk,id_tk,id_tk,
         ERROR_MH_APODEKTO_SYMBOLO,id_tk,id_tk,id_tk,id_tk,id_tk,id_tk,id_tk,id_tk,id_tk,katastasi_letter,id_tk],

    #katastasi_num
        [num_tk,ERROR_PSIFIO_GRAMMA, katastasi_num,num_tk,num_tk,num_tk,num_tk,
         num_tk,num_tk,num_tk,num_tk,num_tk,ERROR_MH_APODEKTO_SYMBOLO,
         num_tk,num_tk,num_tk,num_tk,num_tk,
         num_tk,num_tk,num_tk,num_tk,num_tk,num_tk],

    #katastasi_lessthan
        [lessthan_tk,lessthan_tk,lessthan_tk,lessthan_tk,lessthan_tk,lessthan_tk,lessthan_tk,
         lessthan_tk,lessORequal_tk,lessthan_tk,diaforo_tk,lessthan_tk,ERROR_MH_APODEKTO_SYMBOLO,
         lessthan_tk,lessthan_tk,lessthan_tk,lessthan_tk,lessthan_tk,
         lessthan_tk,lessthan_tk,lessthan_tk,lessthan_tk,lessthan_tk,lessthan_tk],

    #katastasi_greaterthan
        [greaterthan_tk,greaterthan_tk,greaterthan_tk,greaterthan_tk,greaterthan_tk,greaterthan_tk,greaterthan_tk,
         greaterthan_tk,greaterORequal_tk,greaterthan_tk,greaterthan_tk,greaterthan_tk,ERROR_MH_APODEKTO_SYMBOLO,
         greaterthan_tk,greaterthan_tk,greaterthan_tk,greaterthan_tk,greaterthan_tk,
         greaterthan_tk,greaterthan_tk,greaterthan_tk,greaterthan_tk,greaterthan_tk,greaterthan_tk],

     #katastasi_anwkatwteleia
        [anwkatw_teleia_tk,anwkatw_teleia_tk,anwkatw_teleia_tk,anwkatw_teleia_tk,anwkatw_teleia_tk,anwkatw_teleia_tk,
         anwkatw_teleia_tk,anwkatw_teleia_tk,anathesi_tk,anwkatw_teleia_tk,anwkatw_teleia_tk,anwkatw_teleia_tk,
         ERROR_MH_APODEKTO_SYMBOLO,anwkatw_teleia_tk,anwkatw_teleia_tk,anwkatw_teleia_tk,anwkatw_teleia_tk,
         anwkatw_teleia_tk,anwkatw_teleia_tk,anwkatw_teleia_tk,anwkatw_teleia_tk,anwkatw_teleia_tk,anwkatw_teleia_tk,
         anwkatw_teleia_tk],

     #katastasi_sxolia
        [katastasi_sxolia,katastasi_sxolia,katastasi_sxolia,katastasi_sxolia,katastasi_sxolia,katastasi_sxolia,katastasi_sxolia,
         katastasi_sxolia,katastasi_sxolia,katastasi_sxolia,katastasi_sxolia,ERROR_ANOIGMA_SXOLIWN_ME_EOF,katastasi_sxolia,
         katastasi_sxolia,katastasi_sxolia,katastasi_sxolia,katastasi_sxolia,katastasi_sxolia,katastasi_sxolia,katastasi_start,
         katastasi_sxolia,katastasi_sxolia,katastasi_sxolia,katastasi_sxolia]


]


line=1 # trexousa grammi pou diabazei ena xaraktira apo to arxeio


def lex(): # Otan kaleitai epistrefei MONO to amesos epomeno token (sto arxeio cpy pou vriskomai
        global line
        prod_wrd='' # to string tou token
        current= katastasi_start # current = trexousa katastasi
        
        linecounter= line
        resultlex=[]
        while(current>=0 and current<=6): # oso eimai se kapoia katastasi
                char = file.read(1) # diavazei ena xaraktira apo to arxeio

                if (char == ' ' or char == '\t'):
                        char_tk = white_char # char_tk = o akeraios poy antistoixei ston xaraktira
                elif (char in alphabet):
                        char_tk = letters
                elif (char in numbers):
                        char_tk = num
                elif (char == '+'):
                        char_tk = plus
                elif (char == '-'):
                        char_tk = minus
                elif (char == '*'):
                        char_tk = multiply
                elif (char == '/'):
                        char_tk = divide
                elif (char == '%'):
                        char_tk = modulo
                elif(char == '='):
                        char_tk = equal
                elif (char == '<'):
                        char_tk = less_than
                elif (char == '>'):
                        char_tk = greater_than
                elif (char == ''):  # H EOF tha epistrepsei sto telos tou arxeiou   to  ''
                        char_tk = EOF
                elif (char == ','):
                        char_tk = koma
                elif (char == '('):
                        char_tk = arist_parenthesi
                elif (char == ')'):
                        char_tk = deksia_parenthesi
                elif (char == '['):
                        char_tk = arist_aggili
                elif (char == ']'):
                        char_tk = deksia_aggili
                elif (char == '{'):
                        char_tk = anoigma_block
                elif (char == '}'):
                        char_tk = kleisimo_block
                elif (char == '\n'):
                        linecounter=linecounter+1
                        char_tk = allagi_grammis
                elif (char == ':'):
                        char_tk = anwkatw_teleia
                elif (char == '_'):
                        char_tk = katw_paula
                elif (char == ';'):
                        char_tk = erotimatiko
                else:
                        char_tk = oxi_apodekto_simvolo

                #print('Trexousa katastasi ', current )
                #print('Vlepo xaraktira ', char )

                current=pinakas_metavasewn[current][char_tk]

                #print('Nea katastasi ', current)
                #input("Press Enter to continue...")

                if(len(prod_wrd)<30): # mexri 30 grammata krataei (ekfonisi)
                        if(current!=katastasi_start and current!=katastasi_sxolia):
                              prod_wrd+=char # prosthetei to xaraktira sto string tou token
                else:
                        current=ERROR_PANW_APO_30_CHARAKTIRES


#Mexri edw exw brei token!!!!!!!

        if(current==id_tk or current==num_tk or current==lessthan_tk or current==greaterthan_tk or current==anwkatw_teleia_tk):
                if (char == '\n'):
                        linecounter -= 1
                file.seek(file.tell()-1,0)  #epistrefei to teleutaio char pou diabase sto File (px avd+)
                prod_wrd = prod_wrd[:-1]        #kovei to + apo to avd+



        if(current==id_tk):
                if(prod_wrd=='πρόγραμμα'):
                    current=program_tk
                elif(prod_wrd=='δήλωση'):
                    current=declare_tk
                elif (prod_wrd == 'εάν'):
                        current = if_tk
                elif (prod_wrd == 'τότε'):
                        current = then_tk
                elif (prod_wrd == 'αλλιώς'):
                        current = else_tk
                elif (prod_wrd == 'εάν_τέλος'):
                        current = endif_tk
                elif (prod_wrd == 'επανάλαβε'):
                        current = repeat_tk
                elif (prod_wrd == 'μέχρι'):
                        current = until_tk
                elif (prod_wrd == 'όσο'):
                        current = while_tk
                elif (prod_wrd == 'όσο_τέλος'):
                        current = endwhile_tk
                elif (prod_wrd == 'για'):
                        current = for_tk
                elif (prod_wrd == 'έως'):
                        current = to_tk
                elif (prod_wrd == 'με_βήμα'):
                        current = step_tk
                elif (prod_wrd == 'για_τέλος'):
                        current = endfor_tk
                elif (prod_wrd == 'γράψε'):
                        current = print_tk
                elif (prod_wrd == 'διάβασε'):
                        current = input_tk
                elif (prod_wrd == 'και'):
                        current = and_tk
                elif (prod_wrd == 'ή'):
                        current = or_tk
                elif (prod_wrd == 'όχι'):
                        current = not_tk
                elif (prod_wrd == 'συνάρτηση'):
                        current = function_tk
                elif (prod_wrd == 'διαδικασία'):
                        current = procedure_tk
                elif (prod_wrd == 'διαπροσωπεία'):
                        current = interface_tk
                elif (prod_wrd == 'είσοδος'):
                        current = in_tk
                elif (prod_wrd == 'έξοδος'):
                        current = inout_tk
                elif (prod_wrd == 'αρχή_συνάρτησης'):
                        current = beginfunction_tk
                elif (prod_wrd == 'τέλος_συνάρτησης'):
                        current = endfunction_tk
                elif (prod_wrd == 'αρχή_διαδικασίας'):
                        current = beginprocedure_tk
                elif (prod_wrd == 'τέλος_διαδικασίας'):
                        current = endprocedure_tk
                elif (prod_wrd == 'αρχή_προγράμματος'):
                        current = beginprogram_tk
                elif (prod_wrd == 'τέλος_προγράμματος'):
                        current = endprogram_tk
                elif (prod_wrd == 'εκτέλεσε'):
                        current = call_tk

        #ELEGXOS TWN ERRORS
        if(current==ERROR_MH_APODEKTO_SYMBOLO):
                print("ERROR: Exoume mh apodekto symbolo glwssas")
        elif(current==ERROR_PSIFIO_GRAMMA):
                print("ERROR: Akolouthei gramma meta apo kapoio psifio")
        elif(current==ERROR_ANOIGMA_SXOLIWN_ME_EOF):
                print("ERROR: Ta sxolia anoi3an swsta alla den ekleisan sto telos tou arxeiou")
        elif(current==ERROR_PANW_APO_30_CHARAKTIRES):
                print("ERROR: H leksi exei panw apo 30 charaktires")
        elif(current==ERROR_DEKSI_AGGISTRO_MONO_TOU):
                print("ERROR: H leksi einai ena } mono tou")
        elif(current==ERROR_KATW_PAYLA_MONI_TIS):
                print("ERROR: H leksi einai mia _ moni tis")



        #STIN THESH 0 TOY PINAKA EXOUME TO TOKEN
        #STIN THESH 1 TOY PINAKA EXOUME THN LEXH POU SXHMATISE O LEKTIKOS ANALYTHS
        #STIN THESH 2 TOY PINAKA EXOUME TON ARITHMO GRAMMHS

        resultlex.append(current)
        resultlex.append(prod_wrd)
        resultlex.append(linecounter)
        line=linecounter

        print(resultlex)
        #input("Press Enter to continue.")
        return resultlex # epistrefei tin 3ada


'''while(1):
        lexres = lex() # na vgoune stin othoni OLA ta tokens
        if (lexres[0] == EOF_tk):
                break
        print(lexres)
'''

###############################################################################
#	Synarthseis ENDIAMESOU KWDIKA:											  #
###############################################################################
global listOfAllQuads		#lista me Oles tis tetrades pou tha paraxthoun apo to programma.
listOfAllQuads = []         #arxikopoiisi
countQuad = 1				#O arithmos pou xarakthrizei thn tetrada. Brisketai mprosta apo thn 4ada.

def nextQuad():
	'Epistrefei ton arithmo ths epomenhs tetradas pou prokyptei otan paraxthei.'
	global countQuad
	
	return countQuad

listOfAllQuadsFinal = []
def genQuad(first, second, third, fourth):
	'Dhmiourgei thn epomenh 4ada.'
	'Prwto stoixeio sth lista tha balw ton arithmo ths nextQuad(), ousiastika tha ginei 5ada.'
	global countQuad
	global listOfAllQuads
	global listOfAllQuadsFinal
	list = []
	
	list = [nextQuad()]			#Bazw prwta ton arithmo.
	list += [first] + [second] + [third] + [fourth]		#Epeita ta orismata
	
	countQuad +=1	#Ayksanw kata 1 ton arithmo ths epomenhs 4adas.
	listOfAllQuads += [list] 	#Put quad in global listOfAllQuads.
	listOfAllQuadsFinal += [list] 	#Put quad in global listOfAllQuadsFinal gia to telos.
	return list

T_i = 1         #O arithmos tis prosorinis metavlitis.
def newTemp():
	'Dhmiourgei kai epistrefei mia nea proswrinh metablhth, ths morfhs T_1, T_2,.. .'
	global T_i
	global listOfTempVariables
	
	list = ['T_']
	list.append(str(T_i))
	tempVariable="".join(list)
	T_i +=1

	ent = Entity()								#Create an Entity
	ent.type = 'TEMP'							#
	ent.name = tempVariable						#
	ent.tempVar.offset = compute_offset()		#
	new_entity(ent)								#

	return tempVariable

def emptyList():
	'Dhmiourgei mia kenh lista etiketwn 4dwn.'
	pointerList = []	#Arxikopoihsh pointer list.
	
	return pointerList

def makeList(x):
	'Dhmiourgei mia lista etiketwn tetradwn pou periexei mono to x.'
	
	listThis = [x]
	
	return listThis

def merge(list1, list2):
	'Dhmiourgei mia lista etiketwn 4dwn apo th synenwsh listwn list1, list2.'
	list=[]
	list += list1 + list2

	return list

def backPatch(list, z):
	'H lista "list" apoteleitai apo deiktes se tetrades ths listOfAllQuads, twn opoiwn to teleytaio teloumeno Den einai symplhrwmeno.'
	'H backPatch episkeptetai mia mia tis 4des aytes kai tis symplhrwnei me thn etiketa z.'
	'''Prepei na sarwsw th listOfAllQuads kai gia kathe 4ada, pou exei prwto teloumeno arithmo
		pou periexetai sthn list:
		Otan briskw '_' sto 4o teloumeno twn 4dwn aytwn,
		tha to symbplhrwsw me to "z".
	'''
	global listOfAllQuads
	
	for i in range(len(list)):
		for j in range(len(listOfAllQuads)):
			if(list[i]==listOfAllQuads[j][0] and listOfAllQuads[j][4]=='_'):
				listOfAllQuads[j][4] = z
				break;	#to pass second loop faster and enter next i.
	return


###############################################################################
#	Synarthseis PINAKA SYMBOLWN:											  #
###############################################################################	

class Argument():
	' /_\  <- Trigwno'
	def __init__(self):
		self.name = ''		#Dinw to name gia na kserw poio Argument einai.
		self.type = 'Int'	#All variables in this language will be Int (DE xreiazetai).
		self.parMode = ''	# 'CV', 'REF'

class Entity():
	' _ _ 				 '
	'|___|	<- Orthogwnio'
	def __init__(self):
		self.name = ''			#Dinw to name gia na kserw poio Entity einai.
		self.type = ''			#  'VAR' or 'SUBPR' or 'PARAM' or 'TEMP'
		# oi 4 katigories
		self.variable = self.Variable()
		self.subprogram = self.SubProgram()
		self.parameter = self.Parameter()
		self.tempVar = self.TempVar()
		
	class Variable: # metavliti
		def __init__(self):
			self.type = 'Int'           # DE xreiazetai
			self.offset = 0				# Apostash apo thn arxh ths stoibas.
	class SubProgram: # ypoprogramma			
		def __init__(self):
			self.type = ''				# 'Procedure' h' 'Function' .
			self.startQuad = 0			# H proti tetrada tis (apo ton endiameso).
			self.frameLength = 0		# To mhkos eggrafhmatos drasthriopoihshs.
			self.argumentList = []			#h lista parametrwn (gia na apothikeuso ta TRIGONA)
			self.nestingLevel = 0       # gia ton teliko

	class Parameter: # parametros
		def __init__(self):
			self.mode = ''				# 'CV', 'REF'
			self.offset = 0				# Apostash apo thn arxh ths stoibas.
	class TempVar: # prosorini metavliti
		def __init__(self):
			self.type = 'Int'			# DE xreiazetai
			self.offset = 0				# Apostash apo thn arxh ths stoibas.

class Scope():
	'(_)  <- Kyklos'
	def __init__(self):
		self.name = ''						#Dinw to name gia na kserw poio Scope einai.
		self.entityList = []		#h lista apo entities
		self.nestingLevel = 0				# Bathos fwliasmatos.

scopesList = []
def new_argument(object): # ftiahno argument= TRIGONO(galazio)
	'Add given object to list'
	global scopesList

    # scopesList[-1] einai to PIO PANW scope
	# entityList[-1] einai to teleutaio entity = subprogram (function h' procedure)
	scopesList[-1].entityList[-1].subprogram.argumentList.append(object) #add object(TRIGONO) to subprogram.argumentList
	
def new_entity(object):  # ftiahno entity= ORTHOGONIO(kitrino)
	'Add given object to list'
	global scopesList

	scopesList[-1].entityList.append(object)  # sximatika, vazei sto TELOS tis grammis to NEO entity (orthogonio)

def new_scope(name):  # ftiahno KIKLO(kokkino)
	'create new scope'
	global scopesList

	nextScope = Scope()   
	nextScope.name = name

	if( not scopesList ): #arxika None(null)
		nextScope.nestingLevel = 0

	else:
		nextScope.nestingLevel = scopesList[-1].nestingLevel + 1

	scopesList.append(nextScope)

def delete_scope(): # svino KIKLO(kokkino)
	global scopesList

	freeScope = scopesList.pop()
	del freeScope

def compute_offset():
	'Computes how many bytes '
	global scopesList

	counter=0
	if(scopesList[-1].entityList is not []):  # an eho ESTO 1 entity (orthogonio)
		for ent in (scopesList[-1].entityList):  # pigaino se OLA ta entities (orthogonia) tis grammis(optika) pou vriskomai
			if(ent.type == 'VAR' or ent.type == 'TEMP' or ent.type=='PARAM'):  # OXI 'SUBPR' = YPOPROGRAMMA (den exei offset)
				counter +=1  # counter posa orthogonia vrika (horis YPOPROGRAMMA)
	#SizeOf Int variable = 4 and 'Fixed starting size': 3*4=12
	offset = 12+(counter*4)   #12 reserved
	
	return offset

def compute_startQuad():  # kaleite stin "block" META to "begin_block"
	'Compute startQuad (=current Quad) of function or procedure.'
	global scopesList

	#sto apo katw scope(kiklos) sto teleytaio entity (orthogonio einai subprogram) kai enimeronei to startQuad
	scopesList[-2].entityList[-1].subprogram.startQuad = nextQuad()
		
def compute_framelength(): # kaleite stin "block" PRIN to "end_block"
	'Compute frameLength of function or procedure.'
	global scopesList

	#sto apo katw scope(kiklos) sto teleytaio entity (orthogonio einai subprogram) kai enimeronei to frameLength
	scopesList[-2].entityList[-1].subprogram.frameLength = compute_offset()
	
def add_parameters():  # kaleite stin "block" amesos META tin "new_scope" kai metatrepei ta TRIGONA(orismata tis apo katw grammis) se ORTHOGONIA (stin panw-NEA grammi)
	'Create Entities of Parameters of functions or procedures. (ec. in a, inout b)'
	global scopesList

	for arg in scopesList[-2].entityList[-1].subprogram.argumentList: # gia kathe trigwno
		ent = Entity() # ftiakse orthogonio
		ent.name = arg.name
		ent.type = 'PARAM'
		ent.parameter.mode = arg.parMode
		ent.parameter.offset = compute_offset()
		new_entity(ent)

def print_Symbol_table():
	'Prints Symbol-Table: Scopes, Entities, Arguments'
	global scopesList
	global symFile

	symFile.write("########################################################################################")
	symFile.write("\n")

	for sco in reversed(scopesList):
				symFile.write("SCOPE: "+"name:"+sco.name+" nestingLevel:"+str(sco.nestingLevel))
				symFile.write("\n\tENTITIES:\n")
				for ent in sco.entityList:
						if(ent.type == 'VAR'):
								symFile.write("\tENTITY: "+" name:"+ent.name+"\t type:"+ent.type+"\t variable-type:"+ent.variable.type+"\t offset:"+str(ent.variable.offset))
						elif(ent.type == 'TEMP'):
								symFile.write("\tENTITY: "+" name:"+ent.name+"\t type:"+ent.type+"\t temp-type:"+ent.tempVar.type+"\t offset:"+str(ent.tempVar.offset))
						elif(ent.type == 'SUBPR'):
								symFile.write("\tENTITY: "+" name:"+ent.name+"\t type:"+ent.type+"\t subprogram-type:"+ent.subprogram.type+"\t startQuad:"+str(ent.subprogram.startQuad)+"\t frameLength:"+str(ent.subprogram.frameLength))
								symFile.write("\t\tARGUMENTS:")
								for arg in ent.subprogram.argumentList:
										symFile.write("\t\tARGUMENT: "+" name:"+arg.name+"\t type:"+arg.type+"\t parMode:"+arg.parMode)
						elif(ent.type == 'PARAM'):
								symFile.write("\tENTITY: "+" name:"+ent.name+"\t type:"+ent.type+"\t mode:"+ent.parameter.mode+"\t offset:"+str(ent.parameter.offset))
						symFile.write("\n")
				symFile.write("\n\n")
	symFile.write("########################################################################################")
	symFile.write("\n\n\n\n\n")


def search_comb(n): # eikona 1 (sxolia_telikos.zip)
	global scopesList

	for sco in reversed(scopesList):
		for ent in sco.entityList:
			if(ent.name == n):
				return (sco,ent)
	
	print("Den brethike ston pinaka simbolon entity me onoma " + str(n))
	exit(-1)


###############################################################################
#	Synarthseis TELIKOU KODIKA:											      #
###############################################################################
ascFile = open('ascFile.asm','w') # vazw tis entoles telikou kodika (allagi onomatos)
ascFile.write('         \n\n\n') # afino keno wste na mpei to "j Lmain"

def gnlvcode(name):  #DIAFANEIA 24 (pdf)

	global scopesList

	global ascFile

	ascFile.write('lw t0,-4(sp)\n') #stoiva tou gonea

	(sc1,ent1)=search_comb(name) #psaxnei ston pinaka simvolwn na vrei ta (scope,entity) tis metablitis
	
	#/*an einai pappous h' megaliteros progonos,kane to loop "my_help" fores*/
	my_help= scopesList[-1].nestingLevel - sc1.nestingLevel; # an my_help=3 tote einai ston propappou
	my_help=my_help-1 #giati gia ton gonea exoume paragei

	for i in range(0,my_help):
		ascFile.write('lw t0,-4(t0)\n') # an my_help itan 3, to meiwsa kata 1 (egine 2) kai to loop 2 fores

    # pairnw to offset apo ton pinaka simvolwn
	if ent1.type=='VAR':
		x=ent1.variable.offset
	elif ent1.type=='PARAM':
		x=ent1.parameter.offset

	ascFile.write('addi t0,t0,-%d\n' % (x))



def loadvr(v,r): #DIAFANEIES 26 eos 32 (r akeraios, v string)

		global scopesList

		global ascFile

		if v.isdigit():  #DIAFANEIA 26 (panw) αν v είναι σταθερά 
			ascFile.write('li t%d,%s\n' % (r,v))

		else: # allios v einai metavliti
			(sc1,ent1)=search_comb(v)
			
			#DIAFANEIA 26 (katw)
			#sc1.nestingLevel==0 simainei sximatika sto KATW epipedo (main)
			if sc1.nestingLevel==0 and ent1.type=='VAR': # αν v είναι καθολική μεταβλητή – δηλαδή ανήκει στη main
					ascFile.write('lw t%d,-%d(gp)\n' % (r,ent1.variable.offset))
			
			#DIAFANEIA 28 αν v είναι τοπική μεταβλητή, ή τυπική παράμετρος που περνάει με τιμή και βάθος φωλιάσματος ίσο με το τρέχον, ή προσωρινή μεταβλητή
			elif sc1.nestingLevel == scopesList[-1].nestingLevel: #βάθος φωλιάσματος ίσο με το τρέχον
				if ent1.type=='VAR': #αν v είναι τοπική μεταβλητή
						ascFile.write('lw t%d,-%d(sp)\n' % (r,ent1.variable.offset))
						
				elif ent1.type=='TEMP': # αν v είναι προσωρινή μεταβλητή
						ascFile.write('lw t%d,-%d(sp)\n' % (r,ent1.tempVar.offset))
						
				elif ent1.type=='PARAM' and ent1.parameter.mode=='CV': # αν v είναι τυπική παράμετρος που περνάει με τιμή
						ascFile.write('lw t%d,-%d(sp)\n' % (r,ent1.parameter.offset))
						
				#DIAFANEIA 29 αν v είναι τυπική παράμετρος που περνάει με αναφορά
				elif ent1.type=='PARAM' and ent1.parameter.mode=='REF': 
						ascFile.write('lw t0,-%d(sp)\n' % (ent1.parameter.offset))
						ascFile.write('lw t%d,(t0)\n' % (r))
			
			#DIAFANEIA 30 (panw) αν v είναι τοπική μεταβλητή, ή τυπική παράμετρος που περνάει με τιμή και βάθος φωλιάσματος μικρότερο από το τρέχον
			elif sc1.nestingLevel < scopesList[-1].nestingLevel: # βάθος φωλιάσματος μικρότερο από το τρέχον
				if ent1.type=='VAR': #αν v είναι τοπική μεταβλητή
						gnlvcode(v)
						ascFile.write('lw t%d,(t0)\n' % (r))
				elif ent1.type=='PARAM' and ent1.parameter.mode=='CV': # αν v είναι τυπική παράμετρος που περνάει με τιμή
						gnlvcode(v)
						ascFile.write('lw t%d,(t0)\n' % (r))
			
				#DIAFANEIA 30 (katw) αν v είναι τυπική παράμετρος που περνάει με αναφορά
				elif ent1.type=='PARAM' and ent1.parameter.mode=='REF':
						gnlvcode(v)
						ascFile.write('lw t0,(t0)\n')
						ascFile.write('lw t%d,(t0)\n' % (r))


def storerv(r,v):  #DIAFANEIES 34 eos 36 (r akeraios, v string)

	global scopesList
	global ascFile

	(sc1,ent1)=search_comb(v)
	
	#DIAFANEIA 34
	#sc1.nestingLevel==0 simainei sximatika sto KATW epipedo (kirios programma)
	if sc1.nestingLevel==0 and ent1.type=='VAR':
		ascFile.write('sw t%d,-%d(gp)\n' % (r,ent1.variable.offset))
		
	#DIAFANEIA 35 (panw) αν v είναι τοπική μεταβλητή, ή τυπική παράμετρος που περνάει με τιμή και βάθος φωλιάσματος ίσο με το τρέχον, ή προσωρινή μεταβλητή
	elif sc1.nestingLevel == scopesList[-1].nestingLevel: #βάθος φωλιάσματος ίσο με το τρέχον
		if ent1.type=='VAR':
			ascFile.write('sw t%d,-%d(sp)\n' % (r,ent1.variable.offset))
			
		elif ent1.type=='TEMP':
			ascFile.write('sw t%d,-%d(sp)\n' % (r,ent1.tempVar.offset))
			
		elif ent1.type=='PARAM' and ent1.parameter.mode=='CV':
			ascFile.write('sw t%d,-%d(sp)\n' % (r,ent1.parameter.offset))
		
		#DIAFANEIA 35 (katw) αν v είναι τυπική παράμετρος που περνάει με αναφορά
		elif ent1.type=='PARAM' and ent1.parameter.mode=='REF':
			ascFile.write('lw t0,-%d(sp)\n' %  (ent1.parameter.offset))
			ascFile.write('sw t%d,(t0)\n' % (r))

	#DIAFANEIA 36 (panw) αν v είναι τοπική μεταβλητή, ή τυπική παράμετρος που περνάει με τιμή και βάθος φωλιάσματος μικρότερο από το τρέχον
	elif sc1.nestingLevel < scopesList[-1].nestingLevel: # βάθος φωλιάσματος μικρότερο από το τρέχον
		if ent1.type=='VAR':
			gnlvcode(v)
			ascFile.write('sw t%d,(t0)\n' % (r))
		elif ent1.type=='PARAM' and ent1.parameter.mode=='CV':
			gnlvcode(v)
			ascFile.write('sw t%d,(t0)\n' % (r))
			
		#DIAFANEIA 36 (katw) αν v είναι τυπική παράμετρος που περνάει με αναφορά
		elif ent1.type=='PARAM' and ent1.parameter.mode=='REF':
			gnlvcode(v)
			ascFile.write('lw t0,(t0)\n')
			ascFile.write('sw t%d,(t0)\n' % (r))
		
		#DIAFANEIA 41 αν v είναι όνομα συνάρτησης (φέτος ΔΕΝ εχει retv, ara einai PSAGMENO)
		elif ent1.type=='SUBPR' and ent1.subprogram.type == 'Function': 
			# DEN mpainei to loadvr tis diafaneias 41, giati i sinartisi mono apothikeyei
            ascFile.write('lw t0,-8(sp)\n')
			ascFile.write('sw t%d,(t0)\n' % (r))


def search_list_for_call(i): # psaxnei na vrei to "call" (katevainei ena-ena ta "par")

	global listOfAllQuads

	start=i
	while start>=i:

		if (listOfAllQuads[start][1] == 'call'):  # molis vro to "call"
			return str(listOfAllQuads[start][2])  #epistrefo to onoma tou ypoprogrammatos
		
		start=start+1

seira=-1
			
def final():  # tin kalw PANTA META to "end_block" kai prin to "delete_scope"  (mesa stis programblock, funcblock kai procblock)

	global scopesList
	global listOfAllQuads, seira
	global ascFile

	for i in range(len(listOfAllQuads)): # diasxise tis tetrades mexri stigmis (otan kaleitai i final)

		ascFile.write('L' + str(listOfAllQuads[i][0]) + ': \n') # L(arithmos tetradas): (label)

		if (listOfAllQuads[i][1] == 'jump'): #DIAFANEIA 38 (panw)
			ascFile.write('b L'+str(listOfAllQuads[i][4])+'\n')
		elif (listOfAllQuads[i][1] == '='): #DIAFANEIA 38 (katw)
			loadvr(listOfAllQuads[i][2],1) #loadvr(x,1)
			loadvr(listOfAllQuads[i][3],2) #loadvr(y,2)
			ascFile.write('beq,t1,t2,L'+str(listOfAllQuads[i][4])+'\n')
		elif (listOfAllQuads[i][1] == '<>'): #DIAFANEIA 38 (katw)
			loadvr(listOfAllQuads[i][2],1)
			loadvr(listOfAllQuads[i][3],2)
			ascFile.write('bne,t1,t2,L'+str(listOfAllQuads[i][4])+'\n')
		elif (listOfAllQuads[i][1] == '>'): #DIAFANEIA 38 (katw)
			loadvr(listOfAllQuads[i][2],1)
			loadvr(listOfAllQuads[i][3],2)
			ascFile.write('bgt,t1,t2,L'+str(listOfAllQuads[i][4])+'\n')
		elif (listOfAllQuads[i][1] == '<'): #DIAFANEIA 38 (katw)
			loadvr(listOfAllQuads[i][2],1)
			loadvr(listOfAllQuads[i][3],2)
			ascFile.write('blt,t1,t2,L'+str(listOfAllQuads[i][4])+'\n')
		elif (listOfAllQuads[i][1] == '>='):	 #DIAFANEIA 38 (katw)
			loadvr(listOfAllQuads[i][2],1)
			loadvr(listOfAllQuads[i][3],2)
			ascFile.write('bge,t1,t2,L'+str(listOfAllQuads[i][4])+'\n')
		elif (listOfAllQuads[i][1] == '<='): #DIAFANEIA 38 (katw)
			loadvr(listOfAllQuads[i][2],1)
			loadvr(listOfAllQuads[i][3],2)
			ascFile.write('ble,t1,t2,L'+str(listOfAllQuads[i][4])+'\n')	
		elif (listOfAllQuads[i][1] == ':='): #DIAFANEIA 39
			loadvr(listOfAllQuads[i][2],1)
			storerv(1,listOfAllQuads[i][4])
		elif (listOfAllQuads[i][1] == '+'): #DIAFANEIA 40
			loadvr(listOfAllQuads[i][2],1)
			loadvr(listOfAllQuads[i][3],2)
			ascFile.write('add,t1,t1,t2'+'\n')
			storerv(1,listOfAllQuads[i][4])
		elif (listOfAllQuads[i][1] == '-'): #DIAFANEIA 40
			loadvr(listOfAllQuads[i][2],1)
			loadvr(listOfAllQuads[i][3],2)
			ascFile.write('sub,t1,t1,t2'+'\n')
			storerv(1,listOfAllQuads[i][4])
		elif (listOfAllQuads[i][1] == '*'): #DIAFANEIA 40
			loadvr(listOfAllQuads[i][2],1)
			loadvr(listOfAllQuads[i][3],2)
			ascFile.write('mul,t1,t1,t2'+'\n')
			storerv(1,listOfAllQuads[i][4])
		elif (listOfAllQuads[i][1] == '/'): #DIAFANEIA 40
			loadvr(listOfAllQuads[i][2],1)
			loadvr(listOfAllQuads[i][3],2)
			ascFile.write('div,t1,t1,t2'+'\n')
			storerv(1,listOfAllQuads[i][4])
		elif (listOfAllQuads[i][1] == 'out'): #DIAFANEIA 15 (katw)
			loadvr(listOfAllQuads[i][2],1)   # gia na parw to "x"
			ascFile.write('mv a0,t1'+'\n') # den to exei (to t1 na mpei sto a0)
			ascFile.write('li a7,1'+'\n') 
			ascFile.write('ecall'+'\n')
		elif (listOfAllQuads[i][1] == 'inp'): #DIAFANEIA 15 (panw)
			ascFile.write('li a7,5'+'\n')
			ascFile.write('ecall'+'\n')
			ascFile.write('mv t1,a0'+'\n') # den to exei (to a0 na mpei sto t1)
			storerv(1,listOfAllQuads[i][2])    # gia na apothikeuso to "x"

		elif (listOfAllQuads[i][1] == 'par'):  #DIAFANEIA 42 eos 54 [PSAGMENA], OMWS xwris to REF
			if seira==-1:  #DIAFANEIA 42 (PRIN to proto par)
				# prepei na PSAKSO apo tin tetrada "i" pros ta katw to "call", giati ekei vrisketai to onoma
				# tis sinartisis/diadikasias (fname) pou thelo, oste telika na vro to FRAMELENGTH
				fname=search_list_for_call(i)  #[PSAGMENO]
				(sc1,ent1)=search_comb(fname)
				ascFile.write('addi fp,sp,%d\n' % (ent1.subprogram.frameLength))   #FRAMELENGTH
				seira=0   #  arxikopoiisi tou "i"

			if (listOfAllQuads[i][3] == 'CV'):  #DIAFANEIA 44
				loadvr(listOfAllQuads[i][2],0)
				ascFile.write('sw t0,-%d(fp)\n' % (12+4*seira))
				seira=seira+1  # stis diafaneies to exei "i"
			elif (listOfAllQuads[i][3] == 'RET'):
				(sc1,ent1)=search_comb(listOfAllQuads[i][2])   #DIAFANEIA 54
				ascFile.write('addi t0,sp,-%d\n' % (ent1.tempVar.offset))
				ascFile.write('sw t0,-8(fp)\n')
			elif (listOfAllQuads[i][3] == 'REF'):  #DIAFANEIES 45 ews 53
				(sc1,ent1)=search_comb(listOfAllQuads[i][2])  
				
				if sc1.nestingLevel==scopesList[-1].nestingLevel:  #DIAFANEIA 45 kai 47 (ίδιο βάθος φωλιάσματος)
					if ent1.type=='VAR':  #DIAFANEIA 45 
						ascFile.write('addi t0,sp,-%d\n' % (ent1.variable.offset))
						ascFile.write('sw t0,-%d(fp)\n' % (12+4*seira))
					elif ent1.type=='PARAM' and ent1.parameter.mode=='CV':  #DIAFANEIA 45 
						ascFile.write('addi t0,sp,-%d\n' % (ent1.parameter.offset))
						ascFile.write('sw t0,-%d(fp)\n' % (12+4*seira))
					elif ent1.type=='PARAM' and ent1.parameter.mode=='REF':  #DIAFANEIA 47
						ascFile.write('lw t0,-%d(sp)\n' % (ent1.parameter.offset))
						ascFile.write('sw t0,-%d(fp)\n' % (12+4*seira))
						
				elif sc1.nestingLevel<topScope.nestingLevel:  #DIAFANEIA 49 kai 51 (διαφορετικο βάθος φωλιάσματος)
					if ent1.type=='PARAM' and ent1.parameter.mode=='REF':  #DIAFANEIA 51
						gnlvcode(listOfAllQuads[i][2])
						ascFile.write('lw t0,(t0)\n')
						ascFile.write('sw t0,-%d(fp)\n' % (12+4*seira))
					else: #DIAFANEIA 49
						gnlvcode(listOfAllQuads[i][2])
						ascFile.write('sw t0,-%d(fp)\n' % (12+4*seira))
				seira=seira+1
		elif (listOfAllQuads[i][1] == 'call'): #DIAFANEIA 55 eos 60 #[PSAGMENO giati to subprogram.nestingLevel DEN ypirxe ston pinaka simvolon, ara prepei TWRA na mpei stis "def func" kai "def proc"]
			seira=-1 # reset gia mellontika (diladi gia tin epomeni "call")

			(sc1,ent1)=search_comb(listOfAllQuads[i][2])
			if scopesList[-1].nestingLevel==ent1.subprogram.nestingLevel:  #DIAFANEIA 56 (1i periptosi) anadromi (otan i sinartisi kalei ton euato tis)
				ascFile.write('lw t0,-4(sp)\n')
				ascFile.write('sw t0,-4(fp)\n')
			elif scopesList[-1].nestingLevel < ent1.subprogram.nestingLevel:  #DIAFANEIA 59 (2i periptosi)
				ascFile.write('sw sp,-4(fp)\n')
				
			ascFile.write('addi sp,sp,%d\n' % (ent1.subprogram.frameLength)) #DIAFANEIA 60
			ascFile.write('jal L%d\n' % (ent1.subprogram.startQuad))          #DIAFANEIA 60
			ascFile.write('addi sp,sp,-%d\n' % (ent1.subprogram.frameLength)) #DIAFANEIA 60
			
		elif ( listOfAllQuads[i][1] == 'begin_block' and scopesList[-1].nestingLevel!=0):  #DIAFANEIA 61 (panw) [OXI sti main, dld mono se function/procedure]
			ascFile.write('sw ra,(sp)\n')
		elif ( listOfAllQuads[i][1] == 'begin_block' and scopesList[-1].nestingLevel==0):  #DIAFANEIA 62 [TWRA sti main]
			ascFile.seek(0, os.SEEK_SET)
			ascFile.write('j L%d\n'% (listOfAllQuads[i][0]))  #  DIAFANEIA 62 j Lmain , prepei na grafei stin arxi tou arxeiou [ PSAGMENO ]
			ascFile.seek(0, os.SEEK_END)
			
			ascFile.write('addi sp,sp,%d\n' % (compute_offset()))   #DIAFANEIA 62
			ascFile.write('mv gp,sp\n')                            #DIAFANEIA 62
		elif ( listOfAllQuads[i][1] == 'end_block' and scopesList[-1].nestingLevel!=0):  #DIAFANEIA 61 (katw) [OXI sto program, dld mono se function/procedure]
			ascFile.write('lw ra,(sp)\n')
			ascFile.write('jr ra\n')
		elif ( listOfAllQuads[i][1] == 'halt'): #DIAFANEIA 17
			ascFile.write('li a0,0\n')
			ascFile.write('li a7,93\n')
			ascFile.write('ecall\n')

	# reset, giati otan kalw ti final PREPEI na exoun diagrafei oi proigoumenes tetrades METAKSI begin_block kai end_block
	listOfAllQuads = []


#Syntaktikos Analyths (kai PROSTHETW endiameso kwdika KAI pinaka simvolon)

def syntax_an():
        global line
        global lexres

        def program():
                global line 
                global lexres
                
                if(lexres[0] == program_tk):
                        lexres = lex()
                        line = lexres[2]
                        
                        if(lexres[0] == id_tk):
                                id = lexres[1]

                                lexres = lex()
                                line = lexres[2]

                                programblock(id)

                        else:
                                print("ERROR: Den yparxei onoma programmatos",line)
                                exit(-1)
                else:
                         print("ERROR: H leksi 'program' den yparxei stin arxi tou programmatos",line)
                         exit(-1)

        def programblock(name):
                global lexres
                global line

                new_scope(name)

                declarations()
                
                subprograms()
                
                if(lexres[0] == beginprogram_tk):
                        lexres = lex()
                        line = lexres[2]

                        genQuad('begin_block',name,'_','_')
                        sequence()
                        genQuad('halt','_','_','_')
                        genQuad('end_block',name,'_','_')
                        
                        print_Symbol_table()
                        
                        final() # sto telos tis "final" kanw reset ti lista listOfAllQuads me tis tetrades. Krataw antigrafo stin listOfAllQuadsFinal mesa stin genquad, wste na paragw sto telos kai to ".int" poy ebgaze o endiamesos.

                        delete_scope()

                        if(lexres[0] == endprogram_tk):
                           lexres = lex()
                           line = lexres[2]
                           
                        else:
                           print("ERROR: H leksi 'τέλος_προγράμματος' den yparxei sto telos tou programmatos",line)
                           exit(-1)

                else:
                    print("ERROR: H leksi 'αρχή_προγράμματος' den yparxei stin arxi tou programmatos",line)
                    exit(-1)

        def declarations():
                global lexres 
                
                while(lexres[0] == declare_tk):
                        lexres = lex()
                        line = lexres[2]
                        
                        varlist(1)

        def varlist(flag):
                global lexres
                global line
                
                if(lexres[0] == id_tk):
                        id = lexres[1]

                        lexres = lex()
                        line = lexres[2]

                        if (flag == 1):  # to kalese i "declarations", ara einai Entity
                            ent = Entity()							#Create an Entity
                            ent.type = 'VAR'						#
                            ent.name = id						#
                            ent.variable.offset = compute_offset()	#
                            new_entity(ent)							#
                        elif (flag == 2):  # to kalese i "formalparlist", ara einai Argument
                            arg = Argument()		#Creation of a new argument. (Pinakas Symbolwn)
                            arg.name = id		#
                            arg.parMode = ''		# akoma DEN gnorizoume, tha enimerothei sta funcinput-funcoutput
                            new_argument(arg)		#
                        elif (flag == 3):  # to kalese i "funcinput", ara einai Argument CV (me timi)
                            for arg in scopesList[-1].entityList[-1].subprogram.argumentList:
                                if (arg.name == id):
                                    arg.parMode = 'CV'		# TWRA vlepoume oti einai CV (me timi)
                        elif (flag == 4):  # to kalese i "funcoutput", ara einai Argument REF (me anafora)
                            for arg in scopesList[-1].entityList[-1].subprogram.argumentList:
                                if (arg.name == id):
                                    arg.parMode = 'REF'		# TWRA vlepoume oti einai REF (me anafora)


                        while(lexres[0] == koma_tk):
                                lexres = lex()
                                line = lexres[2]
                                
                                if(lexres[0] == id_tk):
                                        id = lexres[1]

                                        lexres = lex()
                                        line = lexres[2]


                                        if (flag == 1):  # to kalese i "declarations", ara einai Entity
                                            ent = Entity()							#Create an Entity
                                            ent.type = 'VAR'						#
                                            ent.name = id						#
                                            ent.variable.offset = compute_offset()	#
                                            new_entity(ent)							#
                                        elif (flag == 2):  # to kalese i "formalparlist", ara einai Argument
                                            arg = Argument()		#Creation of a new argument. (Pinakas Symbolwn)
                                            arg.name = id		#
                                            arg.parMode = ''		# akoma DEN gnorizoume, tha enimerothei sta funcinput-funcoutput
                                            new_argument(arg)		#
                                        elif (flag == 3):  # to kalese i "funcinput", ara einai Argument CV (me timi)
                                            for arg in scopesList[-1].entityList[-1].subprogram.argumentList:
                                                if (arg.name == id):
                                                    arg.parMode = 'CV'		# TWRA vlepoume oti einai CV (me timi)
                                        elif (flag == 4):  # to kalese i "funcoutput", ara einai Argument REF (me anafora)
                                            for arg in scopesList[-1].entityList[-1].subprogram.argumentList:
                                                if (arg.name == id):
                                                    arg.parMode = 'REF'		# TWRA vlepoume oti einai REF (me anafora)


                                else:
                                        print("ERROR: Den yparxei id meta to komma", line)
                                        exit(-1)
                
                else:
                    print("ERROR: Den yparxei kapoio id sti dilosi",line)
                    exit(-1)
                
        def subprograms():
                global lexres
                
                while(lexres[0] == function_tk or lexres[0] == procedure_tk):
                        if (lexres[0] == function_tk):
                               func()
                        else:
                               proc()

        def func():
                global lexres
                global line

                if(lexres[0]== function_tk):
                        lexres = lex()
                        line = lexres[2]

                        if(lexres[0]==id_tk):
                                id = lexres[1]

                                lexres = lex()
                                line = lexres[2]

                                if(lexres[0] == arist_parenthesi_tk):
                                        lexres = lex()
                                        line = lexres[2]

                                        ent = Entity()						#Create an Entity
                                        ent.type = 'SUBPR'					#
                                        ent.name = id					#
                                        ent.subprogram.type = 'Function'	#
                                        ent.subprogram.nestingLevel = scopesList[-1].nestingLevel + 1 # gia TELIKO
                                        new_entity(ent)						#

                                        formalparlist()
                        
                                        if(lexres[0] == deksia_parenthesi_tk):
                                                lexres = lex()
                                                line = lexres[2]
                                                funcblock(id)

                                        else:
                                                print("ERROR: Den kleinei h deksia parenthesi meta thn formalparlist",line)
                                                exit(-1)
                                else:
                                        print("ERROR: Den anoigei h aristeri parenthesi prin thn formalparlist",line)
                                        exit(-1)
                        else:
                                print("ERROR: Perimenoume to id meta to function ", line)
                                exit(-1)

        def proc():
                global lexres
                global line

                if(lexres[0]==procedure_tk):
                        lexres=lex()
                        line=lexres[2]
                        
                        if(lexres[0]==id_tk):
                                id = lexres[1]

                                lexres = lex()
                                line = lexres[2]

                                if(lexres[0] == arist_parenthesi_tk):
                                        lexres = lex()
                                        line = lexres[2]

                                        ent = Entity()						#Create an Entity
                                        ent.type = 'SUBPR'					#
                                        ent.name = id					#
                                        ent.subprogram.type = 'Procedure'	#
                                        ent.subprogram.nestingLevel = scopesList[-1].nestingLevel + 1 # gia TELIKO
                                        new_entity(ent)						#

                                        formalparlist()
                        
                                        if(lexres[0] == deksia_parenthesi_tk):
                                                lexres = lex()
                                                line = lexres[2]
                                                procblock(id)

                                        else:
                                                print("ERROR: Den kleinei h deksia parenthesi meta thn formalparlist",line)
                                                exit(-1)
                                else:
                                        print("ERROR: Den anoigei h aristeri parenthesi prin thn formalparlist",line)
                                        exit(-1)
                        else:
                                print("ERROR: Perimenoume to id meta to procedure ", line)
                                exit(-1)

        def formalparlist():
                global lexres
                
                if(lexres[0] == id_tk):
                    varlist(2)

        def funcblock(name):
                global lexres
                global line

                if(lexres[0] == interface_tk):
                        lexres = lex()
                        line = lexres[2]

                        funcinput()
                        funcoutput()

                        new_scope(name)
                        add_parameters()

                        declarations()
                        subprograms()

                        if(lexres[0] == beginfunction_tk):
                           lexres = lex()
                           line = lexres[2]

                           compute_startQuad()
                           genQuad('begin_block',name,'_','_')
                           sequence()
                           compute_framelength()
                           genQuad('end_block',name,'_','_')

                           print_Symbol_table()
                           
                           final() # sto telos tis "final" kanw reset ti lista listOfAllQuads me tis tetrades. Krataw antigrafo stin listOfAllQuadsFinal mesa stin genquad, wste na paragw sto telos kai to ".int" poy ebgaze o endiamesos.
                           
                           delete_scope()

                           if(lexres[0] == endfunction_tk):
                              lexres = lex()
                              line = lexres[2]
                           
                           else:
                              print("ERROR: H leksi 'τέλος_συνάρτησης' den yparxei sto telos tis sinartisis",line)
                              exit(-1)

                        else:
                           print("ERROR: H leksi 'αρχή_συνάρτησης' den yparxei stin arxi tis sinartisis",line)
                           exit(-1)
                else:
                      print("ERROR: H leksi 'διαπροσωπεία' den yparxei stin arxi tis sinartisis",line)
                      exit(-1)

        def procblock(name):
                global lexres
                global line

                if(lexres[0] == interface_tk):
                        lexres = lex()
                        line = lexres[2]

                        funcinput()
                        funcoutput()
                        
                        new_scope(name)
                        add_parameters()

                        declarations()
                        subprograms()

                        if(lexres[0] == beginprocedure_tk):
                           lexres = lex()
                           line = lexres[2]

                           compute_startQuad()
                           genQuad('begin_block',name,'_','_')
                           sequence()
                           compute_framelength()
                           genQuad('end_block',name,'_','_')

                           print_Symbol_table()

                           final() # sto telos tis "final" kanw reset ti lista listOfAllQuads me tis tetrades. Krataw antigrafo stin listOfAllQuadsFinal mesa stin genquad, wste na paragw sto telos kai to ".int" poy ebgaze o endiamesos.

                           delete_scope()

                           if(lexres[0] == endprocedure_tk):
                              lexres = lex()
                              line = lexres[2]
                           
                           else:
                              print("ERROR: H leksi 'τέλος_διαδικασίαs' den yparxei sto telos tis diadikasias",line)
                              exit(-1)

                        else:
                           print("ERROR: H leksi 'αρχή_διαδικασίας' den yparxei stin arxi tis diadikasias",line)
                           exit(-1)
                else:
                      print("ERROR: H leksi 'διαπροσωπεία' den yparxei stin arxi tis diadikasias",line)
                      exit(-1)

        def funcinput():
                global lexres

                if(lexres[0] == in_tk):
                        lexres = lex()
                        line = lexres[2]

                        varlist(3)

        def funcoutput():
                global lexres

                if(lexres[0] == inout_tk):
                        lexres = lex()
                        line = lexres[2]

                        varlist(4)

        def sequence():
                global lexres
                global line
                

                statement()
                while(lexres[0] == erotimatiko_tk):
                     lexres = lex()
                     line = lexres[2]
                                
                     statement()

        def statement():
                global lexres
                
                if(lexres[0]==id_tk):
                        assignment_stat()
                elif(lexres[0]==if_tk):
                        if_stat()
                elif(lexres[0]==while_tk):
                        while_stat()
                elif(lexres[0]==repeat_tk):
                        do_stat()
                elif(lexres[0]==for_tk):
                        for_stat()
                elif(lexres[0]==input_tk):
                        input_stat()
                elif(lexres[0]==print_tk):
                        print_stat()
                elif(lexres[0]==call_tk):
                        call_stat()
                else:
                        print("ERROR: H entoli pou dosate den anikei sti glossa",line)
                        exit(-1) 

        def assignment_stat():
                global lexres
                global line
                
                if(lexres[0] == id_tk):
                        myid = lexres[1]

                        lexres = lex()
                        line = lexres[2]
                        
                        if(lexres[0] == anathesi_tk):
                                lexres = lex()
                                line = lexres[2]
                                
                                Eplace =expression()
                                genQuad(':=', Eplace, '_', myid)

                        else:
                                print("ERROR: Prepei na yparxei to symvolo anathesis meta to onoma tis metavlitis", line)
                                exit(-1) 

        def if_stat():
                global lexres
                global line
                
                if(lexres[0] == if_tk):
                        lexres= lex()
                        line = lexres[2]

                        C = condition()
                        backPatch(C[0], nextQuad())

                        if(lexres[0]== then_tk):
                            lexres = lex()
                            line = lexres[2]

                            sequence()
                            
                            ifList = makeList(nextQuad())
                            genQuad('jump', '_', '_', '_')
                            backPatch(C[1], nextQuad())

                            elsepart()

                            backPatch(ifList, nextQuad())

                            if(lexres[0] == endif_tk):
                               lexres= lex()
                               line = lexres[2]
                                        
                            else:
                                print("ERROR: Den yparxei 'εάν_τέλος' ", line)
                                exit(-1)
                        else:
                            print("ERROR: Den yparxei 'τότε' ", line)
                            exit(-1)

        def elsepart():
                global lexres
                global line
                
                if(lexres[0] == else_tk):
                        lexres = lex()
                        line = lexres[2]

                        sequence()

        def while_stat():
                global lexres
                global line
                
                if(lexres[0]== while_tk):
                        lexres = lex()
                        line = lexres[2]

                        Cquad=nextQuad()

                        C = condition()

                        backPatch(C[0], nextQuad())

                        if(lexres[0] == repeat_tk):
                             lexres = lex()
                             line = lexres[2]

                             sequence()

                             genQuad('jump', '_', '_', Cquad)
                             backPatch(C[1], nextQuad())

                             if(lexres[0] == endwhile_tk):
                                lexres= lex()
                                line = lexres[2]
                             else:
                                print("ERROR: Den yparxei 'όσο_τέλος' ", line)
                                exit(-1)

                        else:
                            print("ERROR: Den yparxei 'επανάλαβε' ", line)
                            exit(-1)


        def do_stat():
                global lexres
                global line
                
                if(lexres[0] == repeat_tk):
                        lexres = lex()
                        line = lexres[2]

                        Cquad=nextQuad()

                        sequence()

                        if(lexres[0] == until_tk):
                            lexres = lex()
                            line = lexres[2]

                            C = condition()

                            backPatch(C[1], Cquad)
                            backPatch(C[0], nextQuad())

                        else:
                            print("ERROR: Den yparxei 'μέχρι' ", line)
                            exit(-1)

        def for_stat():
                global lexres
                global line
                
                if(lexres[0] == for_tk):
                        lexres = lex()
                        line = lexres[2]
                        
                        if(lexres[0] == id_tk):
                                myid = lexres[1]

                                lexres = lex()
                                line = lexres[2]
                                
                                if(lexres[0] == anathesi_tk):
                                        lexres = lex()
                                        line = lexres[2]
                                        
                                        Eplace1 = expression()

                                        genQuad(':=',Eplace1, '_', myid)

                                        if(lexres[0] == to_tk):
                                                lexres = lex()
                                                line = lexres[2]

                                                Eplace2 = expression()

                                                st = step()

                                                Cquad=nextQuad()  # na epistrepsei gia tin EPOMENI epanalipsi

                                                L_exp_positive = makeList(nextQuad())
                                                genQuad('>', st, '0', '_')     # an step > 0, na paei sto A
                                                L_exp_negative = makeList(nextQuad())
                                                genQuad('<', st, '0', '_')     # an step < 0, na paei sto B
                                                L_exp_zero = makeList(nextQuad())
                                                genQuad('=', st, '0', '_')     # an step = 0, na paei sto C

                                                backPatch(L_exp_positive, nextQuad())      # A (kserw oti step > 0)
                                                L_check_pos_out = makeList(nextQuad())
                                                genQuad('>=', myid, Eplace2, '_')  # an myid >= Eplace2, na paei sto D (termatizei)
                                                L_check_pos_in = makeList(nextQuad())
                                                genQuad('jump', '_', '_', '_')     # alliws, ektelei na paei sto E (sequence)

                                                backPatch(L_exp_negative, nextQuad())      # B (kserw oti step < 0)
                                                L_check_neg_out = makeList(nextQuad())
                                                genQuad('<=', myid, Eplace2, '_')  # an myid <= Eplace2, na paei sto D (termatizei)
                                                L_check_neg_in = makeList(nextQuad())
                                                genQuad('jump', '_', '_', '_')     # alliws, ektelei na paei sto E (sequence)

                                                backPatch(L_exp_zero, nextQuad())          # C (kserw oti step = 0)
                                                                                           # de xreiazetai elegxos otan step = 0, pigainei sequence

                                                if(lexres[0] == repeat_tk):
                                                      lexres = lex()
                                                      line = lexres[2]

                                                      backPatch(L_check_pos_in, nextQuad())  # E
                                                      backPatch(L_check_neg_in, nextQuad())  # E

                                                      sequence()

                                                      genQuad('+', myid, st, myid)  # nea timi sto id: new_id = old_id + step
                                                      genQuad('jump', '_', '_', Cquad)

                                                      backPatch(L_check_pos_out, nextQuad())  # D
                                                      backPatch(L_check_neg_out, nextQuad())  # D

                                                      if(lexres[0] == endfor_tk):
                                                          lexres = lex()
                                                          line = lexres[2]
                                                      else:
                                                        print("ERROR: Den yparxei 'για_τέλος' ", line)
                                                        exit(-1)

                                                else:
                                                     print("ERROR: Den yparxei 'επανάλαβε' ", line)
                                                     exit(-1)


                                        else:
                                            print("ERROR: Den yparxei 'έως' ", line)
                                            exit(-1)

                                else:
                                    print("ERROR: Den yparxei ':=' ", line)
                                    exit(-1)

                        else:
                           print("ERROR: Den yparxei id ", line)
                           exit(-1)

        def step():
                global lexres
                global line
                
                if(lexres[0] == step_tk):
                     lexres = lex()
                     line = lexres[2]

                     Eplace3 = expression()
                     return Eplace3

                else:
                     return '1'



        def print_stat():
                global lexres
                global line
                
                if(lexres[0] == print_tk):
                        lexres = lex()
                        line = lexres[2]
                        
                        Eplace =expression()
                        genQuad('out', Eplace, '_', '_')


        def input_stat():
                global lexres
                global line
                
                if(lexres[0] == input_tk):
                     lexres = lex()
                     line = lexres[2]

                     if(lexres[0] == id_tk):
                          myid = lexres[1]

                          lexres = lex()
                          line = lexres[2]

                          genQuad('inp',myid,'_','_')

                     else:
                             print("ERROR: Den yparxei id ", line)
                             exit(-1)


        def call_stat():
                global lexres
                global line
                
                if(lexres[0] == call_tk):
                        lexres = lex()
                        line = lexres[2]
                                
                        if(lexres[0] == id_tk):
                                idName = lexres[1]

                                lexres = lex()
                                line = lexres[2]

                                idtail(idName, 0)
                                genQuad('call', idName, '_', '_')

                        else:
                                print("ERROR: Den yparxei id ", line)
                                exit(-1)

        def idtail(name, poios_tin_kalese): # 0 (tin kalese call apo procedure), 1 (tin kalese metavliti h' function)
                global lexres
                global line
                
                if(lexres[0] == arist_parenthesi_tk ): # an dei (,  einai procedure h' function giati exei (
                        actualpars()

                        if (poios_tin_kalese == 1):
                            w=newTemp()
                            genQuad('par', w, 'RET', '_')
                            genQuad('call', name, '_', '_')
                            return w

                else: # alliws einai metavliti
                    return name

        def actualpars():
                global lexres
                global line
                
                if(lexres[0] == arist_parenthesi_tk ):
                        lexres = lex()
                        line = lexres[2]

                        actualparlist()

                        if(lexres[0]==deksia_parenthesi_tk):
                                lexres = lex()
                                line = lexres[2]
                        else:
                           print("ERROR: Den kleinei h )",line)
                           exit(-1)

        def actualparlist():
                global lexres
                global line 
                
                actualparitem()
                
                while(lexres[0] == koma_tk):
                        lexres  = lex()
                        line = lexres[2]
                        
                        actualparitem()

                
        def actualparitem():
                global lexres
                global line

                if(lexres[0] == modulo_tk):
                        lexres = lex()
                        line = lexres[2]
                        
                        if(lexres[0] == id_tk):
                                name = lexres[1]

                                lexres = lex()
                                line = lexres[2]

                                genQuad('par', name, 'REF', '_')
                        else:
                                print("ERROR: Perimenei kanonika onoma metavlitis meta to '%' ", line)
                                exit(-1)

                else:
                        thisExpression = expression()
                        genQuad('par', thisExpression, 'CV', '_')

        def condition():
                global lexres
                global line
                
                BT1 = boolterm()

                Ctrue = BT1[0]
                Cfalse = BT1[1]

                while(lexres[0]==or_tk):
                        lexres=lex()
                        line = lexres[2]

                        backPatch(Cfalse, nextQuad())

                        BT2 = boolterm()

                        Ctrue = merge(Ctrue, BT2[0])
                        Cfalse = BT2[1]

                return Ctrue, Cfalse


        def boolterm():
                global lexres
                global line
                
                BF1 = boolfactor()

                BTtrue = BF1[0]
                BTfalse = BF1[1]

                while(lexres[0]==and_tk):
                        lexres=lex()
                        line = lexres[2]

                        backPatch(BTtrue, nextQuad())

                        BF2 = boolfactor()

                        BTfalse = merge(BTfalse, BF2[1])
                        BTtrue = BF2[0]

                return BTtrue, BTfalse

        def boolfactor():
                global lexres
                global line

                if(lexres[0]==not_tk):
                        lexres=lex()
                        line = lexres[2]
                        
                        if(lexres[0]==arist_aggili_tk):
                                lexres = lex()
                                line = lexres[2]
                                
                                C = condition()

                                BFtrue = C[1]
                                BFfalse = C[0]

                                if(lexres[0]==deksia_aggili_tk):
                                        lexres = lex()
                                        line = lexres[2]
                                        
                                else:
                                        print("ERROR: Den yparxei ] meta tin synthiki stin BOOLFACTOR ",line)
                                        exit(-1)
                        else:
                                print("ERROR: Theloume [ meta to not stin BOOLFACTOR", line)
                                exit(-1)

                elif(lexres[0]==arist_aggili_tk):
                        lexres = lex()
                        line = lexres[2]
                        
                        C = condition()

                        BFtrue = C[0]
                        BFfalse = C[1]

                        if(lexres[0]==deksia_aggili_tk):
                                lexres = lex()
                                line = lexres[2]
                                
                                
                        else:
                                print("ERROR: Den yparxei ] meta tin synthiki stin BOOLFACTOR", line)
                                exit(-1)
                else:
                        Eplace1 = expression()
                        
                        relop = relational_oper()
                        
                        Eplace2 = expression()
                        
                        BFtrue=makeList(nextQuad())
                        genQuad(relop, Eplace1, Eplace2, '_')
                        BFfalse=makeList(nextQuad())
                        genQuad('jump', '_', '_', '_')

                return BFtrue, BFfalse


        def expression():
                global lexres
                global line
                
                opt = optional_sign()

                T1place =term()
                
                if ( opt=='-' ):
                   w = newTemp()
                   genQuad('-', '0', T1place, w)
                   T1place = w

                while(lexres[0]==plus_tk or lexres[0]==minus_tk):
                        plusOrMinus =add_oper()

                        T2place =term()
                        #{P1}:
                        w = newTemp()
                        genQuad(plusOrMinus, T1place, T2place, w)
                        T1place = w

                #{P2}:
                Eplace = T1place
                return Eplace
        
        def term():
                global lexres
                global line
                
                F1place =factor()
                
                while(lexres[0]==multiply_tk or lexres[0]==divide_tk):
                        mulOrDiv =mul_oper()

                        F2place =factor()
                        #{P1}:
                        w=newTemp()
                        genQuad(mulOrDiv, F1place, F2place, w)
                        F1place = w

                #{P2}:
                Tplace =F1place
                return Tplace

        def factor():
                global lexres
                global line
                
                if(lexres[0]==num_tk):
                        fact = lexres[1]

                        lexres = lex()
                        line = lexres[2]

                elif(lexres[0]==arist_parenthesi_tk):
                        lexres = lex()
                        line = lexres[2]

                        Eplace =expression()
                        fact = Eplace

                        if(lexres[0]==deksia_parenthesi_tk):
                                lexres = lex()
                                line = lexres[2]
                                
                        else:
                                print("ERROR: Theloume ) meta to expression stin FACTOR ",line)
                                exit(-1)

                elif(lexres[0]==id_tk):
                        fact_temp = lexres[1]

                        lexres = lex()
                        line = lexres[2]

                        fact = idtail(fact_temp, 1)

                else:
                        print("ERROR: Theloume constant h expression h variable stin FACTOR",line)
                        exit(-1)

                return fact

        def relational_oper():
                global lexres 
                global line

                if(lexres[0]==equal_tk):
                        relop = lexres[1]

                        lexres = lex()
                        line = lexres[2]

                elif(lexres[0]==lessthan_tk):
                        relop = lexres[1]
                        
                        lexres = lex()
                        line = lexres[2]

                elif(lexres[0]==lessORequal_tk):
                        relop = lexres[1]
                        
                        lexres = lex()
                        line = lexres[2]

                elif(lexres[0]==diaforo_tk):
                        relop = lexres[1]
                        
                        lexres = lex()
                        line = lexres[2]

                elif(lexres[0]== greaterthan_tk):
                        relop = lexres[1]
                        
                        lexres = lex()
                        line = lexres[2]

                elif(lexres[0]==greaterORequal_tk):
                        relop = lexres[1]
                        
                        lexres = lex()
                        line = lexres[2]

                else:
                        print("ERROR: Leipei = h < h <= h <> h >= h > ",line)
                        exit(-1)

                return relop

        def add_oper():
                global lexres 
                global line
                
                if(lexres[0]==plus_tk):
                        addOp = lexres[1]

                        lexres = lex()
                        line = lexres[2]

                elif(lexres[0]==minus_tk):
                        addOp = lexres[1]

                        lexres = lex()
                        line = lexres[2]

                return addOp

        def mul_oper():
                global lexres 
                global line
                
                if (lexres[0] == multiply_tk):
                        oper = lexres[1]

                        lexres = lex()
                        line = lexres[2]

                elif (lexres[0] == divide_tk):
                        oper = lexres[1]

                        lexres = lex()
                        line = lexres[2]

                return oper

        def optional_sign():
                global lexres
                global line

                if(lexres[0] == plus_tk or lexres[0] == minus_tk):
                       addOp =add_oper()
                       return addOp
                else:
                       return '+'


        lexres= lex()
        line = lexres[2]
        program()


def intCode(intF):
	'Write listOfAllQuadsFinal at intFile.int'
	for i in range(len(listOfAllQuadsFinal)):
		quad = listOfAllQuadsFinal[i]
		intF.write(str(quad[0]))
		intF.write(":  ")
		intF.write(str(quad[1]))
		intF.write("  ")
		intF.write(str(quad[2]))
		intF.write("  ")
		intF.write(str(quad[3]))
		intF.write("  ")
		intF.write(str(quad[4]))
		intF.write("\n")



intFile = open('intFile.int', 'w')
symFile = open('symFile.sym', 'w')

syntax_an()
#telos syntaktikou analyti
print("OK")

intCode(intFile)

symFile.close()
intFile.close()
ascFile.close()
