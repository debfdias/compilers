# Generated from antlr4-python3-runtime-4.7.2/src/autogen/Grammar.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .GrammarParser import GrammarParser
else:
    from GrammarParser import GrammarParser

# This class defines a complete generic visitor for a parse tree produced by GrammarParser.

'''
COMO RESGATAR INFORMAÇÕES DA ÁRVORE

Observe o seu Grammar.g4. Cada regra sintática gera uma função com o nome corespondente no Visitor e na ordem em que está na gramática.

Se for utilizar sua gramática do projeto 1, por causa de conflitos com Python, substitua as regras file por fiile e type por tyype. Use prints temporários para ver se está no caminho certo.  
"make tree" agora desenha a árvore sintática, se quiser vê-la para qualquer input, enquanto "make" roda este visitor sobre o a árvore gerada a partir de Grammar.g4 alimentada pelo input.

Exemplos:

# Obs.: Os exemplos abaixo utilizam nós 'expression', mas servem apra qualquer tipo de nó

self.visitChildren(ctx) # visita todos os filhos do nó atual
expr = self.visit(ctx.expression())  # visita a subárvore do nó expression e retorna o valor retornado na função "visitRegra"

for i in range(len(ctx.expression())): # para cada expressão que este nó possui...
    ident = ctx.expression(i) # ...pegue a i-ésima expressão


if ctx.FLOAT() != None: # se houver um FLOAT (em vez de INT ou VOID) neste nó (parser)
    return Type.FLOAT # retorne tipo float

ctx.identifier().getText()  # Obtém o texto contido no nó (neste caso, será obtido o nome do identifier)

token = ctx.identifier(i).IDENTIFIER().getPayload() # Obtém o token referente à uma determinada regra léxica (neste caso, IDENTIFIER)
token.line      # variável com a linha do token
token.column    # variável com a coluna do token
'''


# Dica: Retorne Type.INT, Type.FLOAT, etc. Nos nós e subnós das expressões para fazer a checagem de tipos enquanto percorre a expressão.
class Type:
    VOID = "void"
    INT = "int"
    FLOAT = "float"
    STRING = "char *"


# This class defines a complete generic visitor for a parse tree produced by GrammarParser.
class GrammarCheckerVisitor(ParseTreeVisitor):
    ids_defined = {} # armazenar informações necessárias para cada identifier definido
    inside_what_function = ""

    # Visit a parse tree produced by GrammarParser#fiile.
    def visitFiile(self, ctx:GrammarParser.FiileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#function_definition.
    def visitFunction_definition(self, ctx:GrammarParser.Function_definitionContext):
        tyype = ctx.tyype().getText()
        name = ctx.identifier().getText()
        params = self.visit(ctx.arguments())
        self.ids_defined[name] = tyype, params, None
        self.inside_what_function = name
        self.visit(ctx.body())
        return


    # Visit a parse tree produced by GrammarParser#body.
    def visitBody(self, ctx:GrammarParser.BodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#statement.
    def visitStatement(self, ctx:GrammarParser.StatementContext):
        if ctx.RETURN() != None:
            token = ctx.RETURN().getPayload()
            tyype, cte_value = self.visit(ctx.expression())
            function_type, params, _ = self.ids_defined[self.inside_what_function]
            if function_type == Type.INT and tyype == Type.FLOAT:
                print("WARNING: possible loss of information returning float expression from int function '" + self.inside_what_function + "' in line " + str(token.line) + " and column " + str(token.column))
            elif function_type == Type.VOID and tyype != Type.VOID:
                print("ERROR: trying to return a non void expression from void function '" + self.inside_what_function + "' in line " + str(token.line) + " and column " + str(token.column))
            elif function_type != Type.VOID and tyype == Type.VOID:
                print("ERROR: trying to return void expression from function '" + self.inside_what_function + "' in line " + str(token.line) + " and column " + str(token.column))

        else:
            self.visitChildren(ctx)
        return


    # Visit a parse tree produced by GrammarParser#if_statement.
    def visitIf_statement(self, ctx:GrammarParser.If_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#else_statement.
    def visitElse_statement(self, ctx:GrammarParser.Else_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#for_loop.
    def visitFor_loop(self, ctx:GrammarParser.For_loopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#for_initializer.
    def visitFor_initializer(self, ctx:GrammarParser.For_initializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#for_condition.
    def visitFor_condition(self, ctx:GrammarParser.For_conditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#for_step.
    def visitFor_step(self, ctx:GrammarParser.For_stepContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#variable_definition.
    def visitVariable_definition(self, ctx:GrammarParser.Variable_definitionContext):
        tyype = ctx.tyype().getText()

        for i in range(len(ctx.identifier())):
            name = ctx.identifier(i).getText()
            token = ctx.identifier(i).IDENTIFIER().getPayload()
            if ctx.expression(i) != None:
                expr_type, cte_value = self.visit(ctx.expression(i))
                if expr_type == Type.VOID:
                    print("ERROR: trying to assign void expression to variable '" + name + "' in line " + str(token.line) + " and column " + str(token.column))
                elif expr_type == Type.FLOAT and tyype == Type.INT:
                    print("WARNING: possible loss of information assigning float expression to int variable '" + name + "' in line " + str(token.line) + " and column " + str(token.column))
            else:
                cte_value = None
            self.ids_defined[name] = tyype, -1, cte_value # -1 means not a array, therefore no length here (vide 15 lines below)

        for i in range(len(ctx.array())):
            name = ctx.array(i).identifier().getText()
            token = ctx.array(i).identifier().IDENTIFIER().getPayload()
            #array_length, _ = self.visit(ctx.array(i))

            if ctx.array_literal(i) != None:
                expr_types, cte_values_array = self.visit(ctx.array_literal(i))
                for j in range(len(expr_types)):
                    if expr_types[j] == Type.VOID:
                        print("ERROR: trying to initialize void expression to array '" + name + "' at index " + str(j) + " of array literal in line " + str(token.line) + " and column " + str(token.column))
                    elif expr_types[j] == Type.FLOAT and tyype == Type.INT:
                        print("WARNING: possible loss of information initializing float expression to int array '" + name + "' at index " + str(j) + " of array literal in line " + str(token.line) + " and column " + str(token.column))
            else:
                cte_values_array = None
            array_length = self.visit(ctx.array(i))
            self.ids_defined[name] = tyype, array_length, cte_values_array

        return


    # Visit a parse tree produced by GrammarParser#variable_assignment.
    def visitVariable_assignment(self, ctx:GrammarParser.Variable_assignmentContext):
        if ctx.identifier() != None:
            name = ctx.identifier().getText()
            token = ctx.identifier().IDENTIFIER().getPayload()
            try:
                tyype, _, cte_value = self.ids_defined[name]
            except:
                print("ERROR: undefined variable '" + name + "' in line " + str(token.line) + " and column " + str(token.column))
                return
        else: # array
            name = ctx.array().identifier().getText()
            token = ctx.array().identifier().IDENTIFIER().getPayload()
            try:
                tyype, array_length, cte_values_array = self.ids_defined[name]
            except:
                print("ERROR: undefined array '" + name + "' in line " + str(token.line) + " and column " + str(token.column))
            array_index = self.visit(ctx.array())
            if cte_values_array != None:
                cte_value = cte_values_array[array_index]
            else:
                cte_value = None

        op = ctx.OP.text
        if op == '++' or op == '--':
          if cte_value is None:
            cte_value = None
          elif op == '++':
            cte_value = eval("{} {} {}".format(cte_value, '+', 1))
          elif op == '--':
            cte_value = eval("{} {} {}".format(cte_value, '-', 1))
        else:
            expr_type, expr_cte_value = self.visit(ctx.expression())
            if expr_type == Type.VOID:
                print("ERROR: trying to assign void expression to variable '" + name + "' in line " + str(token.line) + " and column " + str(token.column))
            elif expr_type == Type.FLOAT and tyype == Type.INT:
                print("WARNING: possible loss of information assigning float expression to int variable '" + name + "' in line " + str(token.line) + " and column " + str(token.column))

            if op == '=':
              cte_value = expr_cte_value
            elif expr_cte_value == None or cte_value == None:
              cte_value = None
            elif op == '/=':
              cte_value = eval("{} {} {}".format(cte_value, '/', expr_cte_value))
            elif op == '*=':
              cte_value = eval("{} {} {}".format(cte_value, '*', expr_cte_value))
            elif op == '+=':
              cte_value = eval("{} {} {}".format(cte_value, '+', expr_cte_value))
            elif op == '-=':
              cte_value = eval("{} {} {}".format(cte_value, '-', expr_cte_value))
            else:
              cte_value = eval("{} {} {}".format(cte_value, op, expr_cte_value))

        if ctx.identifier() != None:
            self.ids_defined[name] = tyype, -1, cte_value
        else: 
            if cte_values_array != None:
                cte_values_array[array_index] = cte_value
            self.ids_defined[name] = tyype, array_length, cte_values_array
        return


    # Visit a parse tree produced by GrammarParser#expression.
    def visitExpression(self, ctx:GrammarParser.ExpressionContext):
        tyype = Type.VOID
        token = None
        cte_value = None 
        if len(ctx.expression()) == 0:

            if ctx.integer() != None:
                tyype = Type.INT
                cte_value = int(ctx.integer().getText())

            elif ctx.floating() != None:
                tyype = Type.FLOAT
                cte_value = float(ctx.floating().getText())

            elif ctx.string() != None:
                tyype = Type.STRING

            elif ctx.identifier() != None:
                name = ctx.identifier().getText()
                try:
                    tyype, _, cte_value = self.ids_defined[name]
                except:
                    token = ctx.identifier().IDENTIFIER().getPayload()
                    print("ERROR: undefined variable '" + name + "' in line " + str(token.line) + " and column " + str(token.column))

            elif ctx.array() != None:
                name = ctx.array().identifier().getText()
                try:
                    tyype, array_length, cte_values_array = self.ids_defined[name]
                except:
                    token = ctx.array().identifier().IDENTIFIER().getPayload()
                    print("ERROR: undefined array '" + name + "' in line " + str(token.line) + " and column " + str(token.column))

                array_index = self.visit(ctx.array())

                if array_index != None and array_length != None:
                    if array_index < 0 or array_index >= array_length:
                        print("ERROR:  array '" + name + "' index out of bounds in line " + str(token.line) + " and column " + str(token.column) + "\n")
                    else:
                        cte_value = cte_values_array[array_index]

            elif ctx.function_call() != None:
                tyype, cte_value = self.visit(ctx.function_call())

        elif len(ctx.expression()) == 1:

            if ctx.OP != None: 
                text = ctx.OP.text
                token = ctx.OP
                tyype, cte_value = self.visit(ctx.expression(0))

                if tyype == Type.VOID:
                    print("ERROR: unary operator '" + text + "' used on type void in line " + str(token.line) + " and column " + str(token.column))
                elif cte_value != None:
                    if text == '-':
                        cte_value = -cte_value
                else:
                    cte_value = None

            else: 
                tyype, cte_value = self.visit(ctx.expression(0))


        elif len(ctx.expression()) == 2: 
            text = ctx.OP.text
            token = ctx.OP
            left, left_cte_value = self.visit(ctx.expression(0))
            right, right_cte_value = self.visit(ctx.expression(1))
            if left == Type.VOID or right == Type.VOID:
                print("ERROR: binary operator '" + text + "' used on type void in line " + str(token.line) + " and column " + str(token.column))

            if text == '*' or text == '/' or text == '+' or text == '-':
                if left == Type.FLOAT or right == Type.FLOAT:
                    tyype = Type.FLOAT
                else:
                    tyype = Type.INT

                if left_cte_value != None and right_cte_value != None:
                    if text == '*':
                        cte_value = left_cte_value * right_cte_value
                    elif text == '/':
                        cte_value = left_cte_value / right_cte_value
                    elif text == '+':
                        cte_value = left_cte_value + right_cte_value
                    elif text == '-':
                        cte_value = left_cte_value - right_cte_value
            else:
                tyype = Type.INT
                if left_cte_value != None and right_cte_value != None:
                    if text == '<':
                        if left_cte_value < right_cte_value:
                            cte_value = 1
                        else:
                            cte_value = 0
                    elif text == '>':
                        if left_cte_value > right_cte_value:
                            cte_value = 1
                        else:
                            cte_value = 0
                    elif text == '==':
                        if left_cte_value == right_cte_value:
                            cte_value = 1
                        else:
                            cte_value = 0
                    elif text == '!=':
                        if left_cte_value != right_cte_value:
                            cte_value = 1
                        else:
                            cte_value = 0
                    elif text == '<=':
                        if left_cte_value <= right_cte_value:
                            cte_value = 1
                        else:
                            cte_value = 0
                    elif text == '>=':
                        if left_cte_value >= right_cte_value:
                            cte_value = 1
                        else:
                            cte_value = 0
                else:
                    cte_value = None

        return tyype, cte_value


    # Visit a parse tree produced by GrammarParser#array.
    def visitArray(self, ctx:GrammarParser.ArrayContext):
        tyype, cte_value = self.visit(ctx.expression())
        if tyype != Type.INT:
            token = ctx.identifier().IDENTIFIER().getPayload()
            print("ERROR: array expression must be an integer, but it is " + str(tyype) + " in line " + str(token.line) + " and column " + str(token.column))
        return cte_value


    # Visit a parse tree produced by GrammarParser#array_literal.
    def visitArray_literal(self, ctx:GrammarParser.Array_literalContext):
        types = []
        cte_values_array = []
        for i in range(len(ctx.expression())):
            tyype, cte_value = self.visit(ctx.expression(i))
            types += [tyype]
            cte_values_array += [cte_value]
        return types, cte_values_array


    # Visit a parse tree produced by GrammarParser#function_call.
    def visitFunction_call(self, ctx:GrammarParser.Function_callContext):
        name = ctx.identifier().getText()
        token = ctx.identifier().IDENTIFIER().getPayload()
        try:
            tyype, args, cte_value = self.ids_defined[name]
            if len(args) != len(ctx.expression()):
                print("ERROR: incorrect number of parameters for function '" + name + "' in line " + str(token.line) + " and column " + str(token.column) + ". Expecting " + str(len(args)) + ", but " + str(len(ctx.expression())) + " were given")
        except:
            print("ERROR: undefined function '" + name + "' in line " + str(token.line) + " and column " + str(token.column))

        for i in range(len(ctx.expression())):
            arg_type, arg_cte_value = self.visit(ctx.expression(i))
            if i < len(args):
                if arg_type == Type.VOID:
                    print("ERROR: void expression passed as parameter " + str(i) + " of function '" + name + "' in line " + str(token.line) + " and column " + str(token.column))
                elif arg_type == Type.FLOAT and args[i] == Type.INT:
                    print("WARNING: possible loss of information converting float expression to int expression in parameter " + str(i) + " of function '" + name + "' in line " + str(token.line) + " and column " + str(token.column))
        return tyype, cte_value


    # Visit a parse tree produced by GrammarParser#arguments.
    def visitArguments(self, ctx:GrammarParser.ArgumentsContext):
        params = []
        for i in range(len(ctx.identifier())):
            tyype = ctx.tyype(i).getText()
            name = ctx.identifier(i).getText()
            self.ids_defined[name] = tyype, -1, None
            params += [tyype]
        return params


    # Visit a parse tree produced by GrammarParser#tyype.
    def visitTyype(self, ctx:GrammarParser.TyypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#integer.
    def visitInteger(self, ctx:GrammarParser.IntegerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#floating.
    def visitFloating(self, ctx:GrammarParser.FloatingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#string.
    def visitString(self, ctx:GrammarParser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#identifier.
    def visitIdentifier(self, ctx:GrammarParser.IdentifierContext):
        return self.visitChildren(ctx)
