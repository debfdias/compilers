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

class GrammarCheckerVisitor(ParseTreeVisitor):
    ids_defined = {} # Dicionário para armazenar as informações necessárias para cada identifier definido
    inside_what_function = "" # String que guarda a função atual que o visitor está visitando. Útil para acessar dados da função durante a visitação da árvore sintática da função.

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
        self.inside_what_function = None
        return


    # Visit a parse tree produced by GrammarParser#body.
    def visitBody(self, ctx:GrammarParser.BodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#statement.
    def visitStatement(self, ctx:GrammarParser.StatementContext):
        return self.visitChildren(ctx)


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
        for i in range(len(ctx.array())):
            array_text = ctx.array(i).identifier().getText()
            array_token = ctx.array(i).identifier().IDENTIFIER().getPayload()
            self.ids_defined[array_text] = ctx.tyype().getText()

            if ctx.array_literal(i) != None:
                for j in range(len(ctx.array_literal(i).expression())):
                    if ctx.array_literal(i).expression(j) != None:
                        #expr_type = self.visitExpression(ctx.expression(i))
                        array_expr_integer = ctx.array_literal(i).expression(j).integer()
                        array_expr_floating = ctx.array_literal(i).expression(j).floating()
                        array_expr_string = ctx.array_literal(i).expression(j).string()
                        array_expr_function_call = ctx.array_literal(i).expression(j).function_call()

                        array_type = self.ids_defined.get(array_text, Type.VOID)

                        if array_expr_integer != None:
                            if array_type == Type.FLOAT:
                                continue
                            elif array_type == Type.INT:
                                continue
                            else:
                                print("ERROR: trying to initialize '{}' expression to '{}' array '{}' at index {} of array literal in line {} and column {}".format(Type.INT, array_type, array_text, j, str(array_token.line), str(array_token.column)))
                        elif array_expr_floating != None:
                            if array_type == Type.FLOAT:
                                continue
                            elif array_type == Type.INT:
                                print("WARNING: possible loss of information initializing '{}' expression to '{}' array '{}' at index {} of array literal in line {} and column {}".format(Type.FLOAT, array_type, array_text, j, str(array_token.line), str(array_token.column)))
                            else:
                                print("ERROR: trying to initialize '{}' expression to '{}' array '{}' at index {} of array literal in line {} and column {}".format(Type.FLOAT, array_type, array_text, j, str(array_token.line), str(array_token.column)))
                        elif array_expr_string != None:
                            if array_type == Type.STRING:
                                continue
                            else:
                                print("ERROR: trying to initialize '{}' expression to '{}' array '{}' at index {} of array literal in line {} and column {}".format(Type.STRING, array_type, array_text, j, str(array_token.line), str(array_token.column)))
                        elif array_expr_function_call != None:
                            print("FUNCTION CALL")

        for i in range(len(ctx.identifier())):
            text = ctx.identifier(i).getText()
            token = ctx.identifier(i).IDENTIFIER().getPayload()
            self.ids_defined[text] = ctx.tyype().getText()

            if ctx.expression(i) != None:
                #expr_type = self.visitExpression(ctx.expression(i))
                expr_integer = ctx.expression(i).integer()
                expr_floating = ctx.expression(i).floating()
                expr_string = ctx.expression(i).string()
                expr_function_call = ctx.expression(i).function_call()

                var_type = self.ids_defined.get(text, Type.VOID)

                if expr_integer != None:
                    if var_type == Type.FLOAT:
                        continue
                    elif var_type == Type.INT:
                        continue
                    else:
                        print("[ERROR]::[You can not assign type <{}> to type <{}>.] ({},{})".format(Type.INT, var_type, str(token.line), str(token.column)))
                elif expr_floating != None:
                    if var_type == Type.FLOAT:
                        continue
                    elif var_type == Type.INT:
                        print("[WARNING]::[Assignment of type FLOAT to type INT may cause loss of information.] ({},{})".format(str(token.line), str(token.column)))
                    else:
                        print("[ERROR]::[You can not assign type <{}> to type <{}>.] ({},{})".format(Type.FLOAT, var_type, str(token.line), str(token.column)))
                elif expr_string != None:
                    if var_type == Type.STRING:
                        continue
                    else:
                        print("[ERROR]::[You can not assign type <{}> to type <{}>.] ({},{})".format(Type.STRING, var_type, str(token.line), str(token.column)))
                elif expr_function_call != None:
                    print("FUNCTION CALL")

                # if expr_type != var_type:
                #     if var_type == Type.FLOAT and expr_type == Type.INT:
                #         continue
                #     elif var_type == Type.INT and expr_type == Type.FLOAT:
                #         print("[WARNING]::[Assignment of type FLOAT to type INT may cause loss of information.] ({},{})".format(str(token.line), str(token.column)))
                #     else:
                #         print("[ERROR]::[You can not assign type <{}> to type <{}>.] ({},{})".format(expr_type, var_type, str(token.line), str(token.column)))
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#variable_assignment.
    def visitVariable_assignment(self, ctx:GrammarParser.Variable_assignmentContext):
        if ctx.identifier() != None:
            id = ctx.identifier().IDENTIFIER().getText()
            var_type = self.ids_defined.get(id, Type.VOID)
            token = ctx.identifier().IDENTIFIER().getPayload()
            #visitar checar se o identifier e verificar se ele já foi definido. Printar um erro se não foi
            if id not in self.ids_defined:
                print("ERROR: undefined variable '" + id + "' in line {}".format(token.line) + " and column {}".format(token.column))
                return

        if ctx.expression() != None:
            expr_integer = ctx.expression().integer()
            expr_floating = ctx.expression().floating()
            expr_string = ctx.expression().string()
            expr_function_call = ctx.expression().function_call()
            if expr_integer != None:
                if var_type != Type.FLOAT and var_type != Type.INT:
                    print("[ERROR]::[You can not assign type <{}> to type <{}>.] ({},{})".format(Type.INT, var_type, str(token.line), str(token.column)))
            elif expr_floating != None:
                if var_type == Type.INT:
                    print("[WARNING]::[Assignment of type FLOAT to type INT may cause loss of information.] ({},{})".format(str(token.line), str(token.column)))
                elif var_type != Type.FLOAT:
                    print("[ERROR]::[You can not assign type <{}> to type <{}>.] ({},{})".format(Type.FLOAT, var_type, str(token.line), str(token.column)))
            elif expr_string != None:
                if var_type != Type.STRING:
                    print("[ERROR]::[You can not assign type <{}> to type <{}>.] ({},{})".format(Type.STRING, var_type, str(token.line), str(token.column)))
            elif expr_function_call != None:
                print("FUNCTION CALL")
            
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#expression.
    def visitExpression(self, ctx:GrammarParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#array.
    def visitArray(self, ctx:GrammarParser.ArrayContext):
        if ctx.expression().identifier() != None:
            expression_text = ctx.expression().identifier().IDENTIFIER().getText()

            if self.ids_defined[expression_text] == None :
                integer_type = ctx.expression().integer()
                floating_type = ctx.expression().floating()
                string_type = ctx.expression().string()
                if ctx.expression().floating() != None:
                    expr_type = Type.FLOAT
                elif ctx.expression().string():
                    expr_type = Type.STRING

                if integer_type == None:
                    token = ctx.identifier().IDENTIFIER().getPayload()
                    print("ERROR: array expression must be an integer, but it is {} in line {} and column {}".format(expr_type, str(token.line), str(token.column)))
            elif self.ids_defined[expression_text] != Type.INT:
                token = ctx.identifier().IDENTIFIER().getPayload()
                print("ERROR: array expression must be an integer, but it is {} in line {} and column {}".format(self.ids_defined[expression_text], str(token.line), str(token.column)))
        else:
            integer_type = ctx.expression().integer()
            floating_type = ctx.expression().floating()
            string_type = ctx.expression().string()
            if ctx.expression().floating() != None:
                expr_type = Type.FLOAT
            elif ctx.expression().string():
                expr_type = Type.STRING
            #print(integer_type)
            if integer_type == None:
                token = ctx.identifier().IDENTIFIER().getPayload()
                print("ERROR: array expression must be an integer, but it is {} in line {} and column {}".format(expr_type, str(token.line), str(token.column)))
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#array_literal.
    def visitArray_literal(self, ctx:GrammarParser.Array_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#function_call.
    def visitFunction_call(self, ctx:GrammarParser.Function_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarParser#arguments.
    def visitArguments(self, ctx:GrammarParser.ArgumentsContext):
        for i in range(len(ctx.identifier())):
            text = ctx.identifier(i).getText()
            self.ids_defined[text] = ctx.tyype(i).getText()

        return self.visitChildren(ctx)


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

