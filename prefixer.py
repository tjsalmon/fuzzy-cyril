#! /usr/bin/env python
#Write a program that given an infix arithmetic expression, outputs a prefix version.
import sys
import os
#print 'Hello prefixer in {0}'.format(os.getcwd())

f = open('{0}/{1}'.format(os.getcwd(),sys.argv[1]), 'r')
List = f.readline()
print '\nInfix expression: {0}'.format(List)
inExpr = List.split(' ')
inExpr[len(inExpr)-1] = inExpr[len(inExpr)-1].strip('\n')
inExpr.append(';')

class parseTree: 
	def __init__(self, value, left=None, right=None): #Node with value, left tree and right tree
		self.value = value
		self.left = left
		self.right = right

	def __str__(self): #Prints string representing value
		return str(self.value)

def token(expr, match): #If token is expected, consume it
	if (expr[0] == match):
		del expr[0]
		return True
	else:
		return False

def operand(expr): #Consumes an operand whether it's an expression in brackets or a variable
	if (token(expr, '(')):
		x = addsub(expr)
		token(expr, ')')
		return x
	else:
		if  (expr[0].isdigit() or expr[0].isalpha()):
			operand = expr[0]
			del expr[0]
			return parseTree(operand)

def addsub(expr): #Sum/diff can be product on left, sum/diff on right or just a product
	l = muldiv(expr)
	if (token(expr, '+')):
		ra = addsub(expr)
		return parseTree('+', l, ra)
	elif (token(expr, '-')):
		rs = addsub(expr)
		return parseTree('-', l, rs)
	else:
		return l

def muldiv(expr): #Builds an expression of products and quotients
	l = operand(expr)
	if (token(expr, '*')):
		rm = muldiv(expr)
		return parseTree('*', l, rm)
	elif (token(expr, '/')):
		rd = muldiv(expr)
		return parseTree('/', l, rd)
	else:
		return l

def printPrefix(tree): #Preorder tree traversal to print expressions in prefix notation
	output = ''
	if (tree == None):
		return ''
	#print '( {0} )'.format(tree.value),
#	if (tree.value == '*' or tree.value == '/' or tree.value == '+' or tree.value == '-'):
#		print '( {0} )'.format(tree.value),
#	else:
#		print tree.value,
#	print tree.value,
	elif (tree.value.isdigit() or tree.value.isalpha()):
		return '{0}'.format(tree.value)
	output += '({0} '.format(tree.value)
	output += '{0} '.format(printPrefix(tree.left))
	output += '{0})'.format(printPrefix(tree.right))
	return output

preExpr = addsub(inExpr)
print 'Prefix expression:',
print printPrefix(preExpr)
print '\n'