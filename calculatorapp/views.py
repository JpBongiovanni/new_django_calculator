from django.shortcuts import render
from django.db.models import Q
import re
from .models import Calculation


def greetings(request):
    context = {
        "calculations": Calculation.objects.all().order_by('-created_at'),
    }
    res=render(request,'calc.html', context)
    return res

def searchbar(request):
    if request.method == "GET":
        search = request.GET["search"],
        print(search[0])
        calc_res = Calculation.objects.filter(Q(calc_results__icontains=search[0])|Q(calc_values__icontains=search[0]))
        
    return render(request, "calc.html", {"calculations": Calculation.objects.all().order_by('-created_at')[0:20], "calc_res": calc_res})

def calculation(request):
    if request.method=="POST":
        values=request.POST['values'] #the input is gathered as a whole string
        
        vals=re.findall(r"(\d+)",values) #REGEX is then used to isolate the integers
        operators=['+','x','÷','-','.','%']
        opr=[]
        #the for loops below are used to loop through the list of possible operators
        #and the value string. Once a match is found, the operator is identified and then appened
        #into the opr list.
        #Based on what the opr is, the logic changes
        for v in values:            
            for o in operators:
                if v==o:
                    opr.append(o)
        
        for o in opr:
            if o=='.':
                i=opr.index(o)
                res=vals[i]+"."+vals[i+1]
                vals.remove(vals[i+1])
                opr.remove(opr[i])
                vals[i]=res
                
        for o in opr:
            if o=='%':
                i=opr.index(o)
                res=(float(vals[i])/100)*float(vals[i+1])
                vals.remove(vals[i+1])
                opr.remove(opr[i])
                vals[i]=res
                
        for o in opr:
            if o=='÷':
                i=opr.index(o)
                res=float(vals[i])/float(vals[i+1])
                vals.remove(vals[i+1])
                opr.remove(opr[i])
                vals[i]=str(res)
                
        for o in opr:
            if o=='x':
                i=opr.index(o)
                res=float(vals[i])*float(vals[i+1])
                vals.remove(vals[i+1])
                opr.remove(opr[i])
                vals[i]=str(res)
                
        for o in opr:
            if o=='+':
                i=opr.index(o)
                res=float(vals[i])+float(vals[i+1])
                vals.remove(vals[i+1])
                opr.remove(opr[i])
                vals[i]=str(res)

            if o=='-':
                i=opr.index(o)
                res=float(vals[i])-float(vals[i+1])
                vals.remove(vals[i+1])
                opr.remove(opr[i])
                vals[i]=str(res)

        if len(opr)!=0:
            if opr[0]=='÷':
                result = float(vals[0])/float(vals[1])
            elif opr[0]=='x':
                result = float(vals[0])*float(vals[1])
            elif opr[0]=='+':
                result = float(vals[0])+float(vals[1])
            else :
                result = float(vals[0])-float(vals[1])
        else:
            result = float(vals[0])

        final_result=round(result,2)
        
        Calculation.objects.create(
            calc_values = values,
            calc_results = final_result
        )    
        
    res=render(request,'calc.html',{'result':final_result,'values':values, "calculations": Calculation.objects.all().order_by('-created_at')[0:20]})
    
    return res