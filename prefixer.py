#! /usr/bin/env python
#Twitch.TV Internship Challenge Problem
#Write a program that given an infix arithmetic expression, outputs a prefix version.
import sys
import os

if (len(sys.argv) == 3):
	f = open('{0}/{1}'.format(os.getcwd(),sys.argv[2]), 'r')
elif (len(sys.argv) == 2):
	f = open('{0}/{1}'.format(os.getcwd(),sys.argv[1]), 'r')
List = f.readline()
print 'Infix expression: {0}'.format(List)
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

def operand(expr): #Consumes an operand whether it's a subexpression in brackets or a variable
	if (token(expr, '(')):
		x = addsub(expr)
		token(expr, ')')
		return x
	else:
		if  (expr[0].isdigit() or expr[0].isalpha()):
			operand = expr[0]
			del expr[0]
			return parseTree(operand)

def operator(node): #Return true if node is an operator
	if (node == '*' or node == '/' or node == '+' or node == '-'):
		return True
	else:
		return False
	
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

def simplifyTree(tree): #Reduces expressions as much as possible by traversing tree
	if (tree == None):
		return ''
	if (tree.left != None and operator(tree.left.value)):
                tree.left = simplifyTree(tree.left)
        if (tree.right != None and operator(tree.right.value)):
                tree.right = simplifyTree(tree.right) 
	if (tree.left != None and tree.right != None and str(tree.left.value).isdigit() and str(tree.right.value).isdigit()):
		if (tree.value == '*'):
			tree.value = int(tree.left.value) * int(tree.right.value)
		elif (tree.value == '/'):
			tree.value = int(tree.left.value) / int(tree.right.value)
		elif (tree.value == '+'):
			tree.value = int(tree.left.value) + int(tree.right.value)                      
       		elif (tree.value == '-'):
			tree.value = int(tree.left.value) - int(tree.right.value)
	    	tree.left = None
               	tree.right = None
	return tree
		
def printPrefix(tree): #Preorder tree traversal to print expressions in prefix notation
	output = ''
	if (tree == None):
		return ''
	elif (str(tree.value).isdigit() or str(tree.value).isalpha()):
		return '{0}'.format(tree.value)
	output += '({0} '.format(tree.value)
	output += '{0} '.format(printPrefix(tree.left))
	output += '{0})'.format(printPrefix(tree.right))
	return output

def printRaw(tree): #Prints prefix expression with no brackets
	outRaw = ''
	if (tree == None):
                return ''
	outRaw += ('{0} ').format(tree.value)
	outRaw += ('{0}').format(printRaw(tree.left))
	outRaw += ('{0}').format(printRaw(tree.right))
	return outRaw

preExpr = addsub(inExpr)

#print 'Raw prefix expression:',
#print printRaw(preExpr)

if (len(sys.argv) == 3):
	print 'Simplified prefix expression:',
	print printPrefix(simplifyTree(preExpr))
	print
else:
	print 'Prefix expression:',
	print printPrefix(preExpr)
	print
