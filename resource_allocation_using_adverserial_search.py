def parse_applicant(string):
#extracting applicant details
    i=0
    actual_id=string[i:i+5]
    app_id=int(string[i:i+5])
    i=i+5
    gender=string[i]
    i=i+1
    age=int(string[i:i+3])
    i=i+3
    pets=string[i]
    i=i+1
    medic=string[i]
    i=i+1
    car=string[i]
    i=i+1
    licen=string[i]
    i=i+1
    days=[]
    for j in range(7):
        days.append(int(string[j+i]))
    req_days=sum(days)
    #return [app_id,gender,age,pets,medic,car,licen,days,req_days]
    return {"actual_id":actual_id,"id":app_id,"gen":gender,"age":age,"pet":pets,"med":medic,"car":car,"lic":licen,"days":days,"req":req_days,"visited":0}

    
def parse_input():
    f=open("input.txt","r")
    f=f.readlines()
    b=int(f[0])
    b_available_slots=[b for i in range(7)]
    p=int(f[1])
    p_available_slots=[p for i in range(7)]
    b=b*7
    p=p*7
    l=int(f[2])
    l_list=[]
    for i in range(l):
        l_list.append(int(f[i+3]))
    counter=l+3
    s=int(f[counter])
    s_list=[]
    counter=counter+1
    for i in range(s):
        s_list.append(int(f[i+counter]))
    counter=s+counter
    a=int(f[counter])
    a_list=[]
    counter=counter+1
    for i in range(a):
        a_list.append(parse_applicant(f[i+counter]))
    s_candidate_list=[]
    l_candidate_list=[]
    common_candidate_list=[]
    remaining_list=[]
    for k in a_list:
        if k["id"] not in s_list and k["id"] not in l_list:
 #Extracting remaining candidate details
            remaining_list.append(k)
    
    for k in remaining_list:
        if k["age"]>17 and k["gen"]=="F" and k["pet"]=="N" and k["car"]=="Y" and k["lic"]=="Y" and k["med"]=="N":
 #Extracting common candidate details
                common_candidate_list.append(k)
    
    for k in remaining_list:
        if k not in common_candidate_list:
            if k["car"]=="Y" and k["lic"]=="Y" and k["med"]=="N":
#Extracting s candidate details
                s_candidate_list.append(k)
            if k["age"]>17 and k["gen"]=="F" and k["pet"]=="N":
#Extracting l candidate details
                l_candidate_list.append(k)
    
#Representation of remaining beds and car slots    
    b_remaining=b
    p_remaining=p
    for k in a_list:
        if k["id"] in l_list:
            b_available_slots=list(map(lambda x,y:x-y, b_available_slots,k["days"]))
            b_remaining=b_remaining-k["req"]
        if k["id"] in s_list:
            p_available_slots=list(map(lambda x,y:x-y, p_available_slots,k["days"]))
            p_remaining=p_remaining-k["req"]
            
    s_candidate_slots=[0 for i in range(7)]
    l_candidate_slots=[0 for i in range(7)]    
 
    common_candidate_list=sorted(common_candidate_list, key=lambda k:(k['id']))
    s_candidate_list=sorted(s_candidate_list, key=lambda k:(k['id']))
    l_candidate_list=sorted(l_candidate_list, key=lambda k:(k['id']))
    
    return (b,b_available_slots,p,p_available_slots,l,l_list,s,s_list,a,a_list,s_candidate_list,l_candidate_list,common_candidate_list,b_remaining,p_remaining, s_candidate_slots, l_candidate_slots)



'''driver'''
def min_max(common_len,s_len,l_len,common_candidate_list,p_remaining,p_assigned,p_available_slots,s_candidate_list,s_assignment,b_remaining,b_assigned,b_available_slots,l_candidate_list,l_assignment):
    max_val=0
    id_val='100000'
    temp_dict={}
    for i in common_candidate_list:
        temp_str=str(i["days"])
        if i["visited"]==0 and temp_str not in temp_dict:
            temp_dict[temp_str]=1
            temp_check=list(map(lambda x,y:x-y,p_available_slots,i["days"]))
    
            if(min(temp_check)>-1):
                i["visited"]=1
                s_assignment.append(i["actual_id"]);
                (w,x,y,z)=turn_lahsa(common_len-1,s_len,l_len,common_candidate_list,p_remaining-i["req"],p_assigned+i["req"],temp_check,s_candidate_list,s_assignment,b_remaining,b_assigned,b_available_slots,l_candidate_list,l_assignment)
                if(w>max_val) or (w==max_val and int(id_val)>int(i["actual_id"])):
                    max_val,id_val=w,i["actual_id"]
                s_assignment.pop()
                i["visited"]=0
    temp_dict={}
    for i in s_candidate_list:
        temp_str=str(i["days"])
        if i["visited"]==0 and temp_str not in temp_dict:
            temp_dict[temp_str]=1
            temp_check=list(map(lambda x,y:x-y,p_available_slots,i["days"]))
            if(min(temp_check)>-1):
                i["visited"]=1
                s_assignment.append(i["actual_id"]);
                (w,x,y,z)=turn_lahsa(common_len,s_len-1,l_len,common_candidate_list,p_remaining-i["req"],p_assigned+i["req"],temp_check,s_candidate_list,s_assignment,b_remaining,b_assigned,b_available_slots,l_candidate_list,l_assignment)
                if(w>max_val) or (w==max_val and int(id_val)>int(i["actual_id"])):
                    max_val,id_val=w,i["actual_id"]
                i["visited"]=0

    return max_val,id_val
    
    
'''SPLA'''
def turn_spla(common_len,s_len,l_len,common_candidate_list,p_remaining,p_assigned,p_available_slots,s_candidate_list,s_assignment,b_remaining,b_assigned,b_available_slots,l_candidate_list,l_assignment):
    global mapper
    res_p=p_assigned
    res_b=b_assigned
    res_s_assignment=s_assignment[:]
    res_l_assignment=l_assignment[:]
    sorted_s=tuple(sorted(s_assignment[:]))
    sorted_l=tuple(sorted(l_assignment[:]))
    
    if (sorted_s,sorted_l) in mapper:
        temp1,temp2=mapper[sorted_s,sorted_l]
        
        return (temp1,temp2,["halla"],["loua"])
    if(common_len+s_len+l_len==0):
#Final Assignment step

#Updating max assignment of LAHSA assignment
        mapper[sorted_s,sorted_l]=(p_assigned,b_assigned)
        return (p_assigned,b_assigned,s_assignment[:],l_assignment[:])
    if(common_len+s_len==0):
        return turn_lahsa(common_len,s_len,l_len,common_candidate_list,p_remaining,p_assigned,p_available_slots,s_candidate_list,s_assignment,b_remaining,b_assigned,b_available_slots,l_candidate_list,l_assignment)
    
    elif(common_len>0):
        temp_dict={}
        for i in common_candidate_list:
            temp_str=str(i["days"])
            if i["visited"]==0 and temp_str not in temp_dict:
                temp_dict[temp_str]=1
                temp_check=list(map(lambda x,y:x-y,p_available_slots,i["days"]))
             
                if(min(temp_check)>-1):
                    i["visited"]=1
                    s_assignment.append(i["actual_id"]);
                    (w,x,y,z)=turn_lahsa(common_len-1,s_len,l_len,common_candidate_list,p_remaining-i["req"],p_assigned+i["req"],temp_check,s_candidate_list,s_assignment,b_remaining,b_assigned,b_available_slots,l_candidate_list,l_assignment)
                    if(w>res_p):
                        (res_p,res_b,res_s_assignment,res_l_assignment)=(w,x,y,z)
                    s_assignment.pop()
                    i["visited"]=0
        temp_dict={}
        for i in s_candidate_list:
            temp_str=str(i["days"])
            if i["visited"]==0 and temp_str not in temp_dict:
                temp_dict[temp_str]=1
                temp_check=list(map(lambda x,y:x-y,p_available_slots,i["days"]))
                
                if(min(temp_check)>-1):
                    i["visited"]=1
                    s_assignment.append(i["actual_id"]);
                    (w,x,y,z)=turn_lahsa(common_len,s_len-1,l_len,common_candidate_list,p_remaining-i["req"],p_assigned+i["req"],temp_check,s_candidate_list,s_assignment,b_remaining,b_assigned,b_available_slots,l_candidate_list,l_assignment)
                    if(w>res_p):
                            (res_p,res_b,res_s_assignment,res_l_assignment)=(w,x,y,z)
                    s_assignment.pop()
                    i["visited"]=0
                    
    else:
        s_candidate_slots=[0 for i in range(7)]
        for i in s_candidate_list:
            if i["visited"]==0:              
                s_candidate_slots=list(map(lambda x,y:x+y,s_candidate_slots,i["days"]))
                
        l_candidate_slots=[0 for i in range(7)]
        for i in l_candidate_list:
            if i["visited"]==0:              
                l_candidate_slots=list(map(lambda x,y:x+y,l_candidate_slots,i["days"])) 
        res_p,res_s_assignment=spla_alone(s_candidate_slots,s_len,p_remaining,p_assigned,p_available_slots,s_candidate_list,s_assignment,sorted_l,res_b)
        res_b,res_l_assignment=lahsa_alone(l_candidate_slots,l_len,b_remaining,b_assigned,b_available_slots,l_candidate_list,l_assignment,sorted_s,res_p)
                    
    mapper[sorted_s,sorted_l]=(res_p,res_b)
    return (res_p,res_b,res_s_assignment,res_l_assignment)

'''ONLY SPLA'''
def spla_alone(s_candidate_slots,s_len,p_remaining,p_assigned,p_available_slots,s_candidate_list,s_assignment,sorted_l,res_b):
    global mapper
    res_p=p_assigned
    res_s_assignment=s_assignment[:]
    sorted_s=tuple(sorted(s_assignment[:]))
    if (sorted_s,sorted_l) in mapper:
        temp1,temp2=mapper[sorted_s,sorted_l]
        return (temp1,sorted_s)
    if(s_len==0):
        mapper[sorted_s,sorted_l]=(res_p,res_b)
        return (res_p,res_s_assignment)                    
    else:              
        temp_lis=list(map(lambda x,y:x-y,p_available_slots,s_candidate_slots))
        if min(temp_lis)>-1:
            res_p+=sum(s_candidate_slots) 
            temp_assign=[]
            for i in s_candidate_list:
                if i["visited"]==0:              
                    temp_assign.append(i["actual_id"])
            temp_assign=s_assignment+temp_assign
            return res_p,temp_assign
        else:
            temp_dict={}
            for i in s_candidate_list:
                temp_str=str(i["days"])
                if i["visited"]==0 and temp_str not in temp_dict:
                    temp_dict[temp_str]=1
                    temp_check=list(map(lambda x,y:x-y,p_available_slots,i["days"]))
                    if(min(temp_check)>-1):
                        i["visited"]=1
                        s_assignment.append(i["actual_id"]);
                        temp_s_slots=list(map(lambda x,y:x-y,s_candidate_slots,i["days"]))
                        (w,x)=spla_alone(temp_s_slots,s_len-1,p_remaining-i["req"],p_assigned+i["req"],temp_check,s_candidate_list,s_assignment,sorted_l,res_b)
                        
                        if(w>res_p):
                                (res_p,res_s_assignment)=(w,x)
                        s_assignment.pop()
                        i["visited"]=0
    if (sorted_s,sorted_l) not in mapper:
        mapper[sorted_s,sorted_l]=(res_p,res_b)
    return (res_p,res_s_assignment[:])

'''LAHSA'''
def turn_lahsa(common_len,s_len,l_len,common_candidate_list,p_remaining,p_assigned,p_available_slots,s_candidate_list,s_assignment,b_remaining,b_assigned,b_available_slots,l_candidate_list,l_assignment):
    global mapper
    res_p=p_assigned
    res_b=b_assigned
    res_s_assignment=s_assignment[:]
    res_l_assignment=l_assignment[:]
    sorted_s=tuple(sorted(s_assignment[:]))
    sorted_l=tuple(sorted(l_assignment[:]))
    
    if (sorted_s,sorted_l) in mapper:
        temp1,temp2=mapper[sorted_s,sorted_l]
        return (temp1,temp2,["lahsa"],["loua"])
    
    if(common_len+s_len+l_len==0):
        mapper[sorted_s,sorted_l]=(p_assigned,b_assigned)
        return (p_assigned,b_assigned,s_assignment[:],l_assignment[:])
    
    if(common_len+l_len==0):
        return turn_spla(common_len,s_len,l_len,common_candidate_list,p_remaining,p_assigned,p_available_slots,s_candidate_list,s_assignment,b_remaining,b_assigned,b_available_slots,l_candidate_list,l_assignment)
    elif(common_len>0):
        temp_dict={}
        for i in common_candidate_list:
            temp_str=str(i["days"])
            if i["visited"]==0 and temp_str not in temp_dict:
                temp_dict[temp_str]=1
                temp_check=list(map(lambda x,y:x-y,b_available_slots,i["days"]))
          
                if(min(temp_check)>-1):
                    i["visited"]=1
                    l_assignment.append(i["actual_id"]);
                    (w,x,y,z)=turn_spla(common_len-1,s_len,l_len,common_candidate_list,p_remaining,p_assigned,p_available_slots,s_candidate_list,s_assignment,
                    b_remaining-i["req"],b_assigned+i["req"],temp_check,l_candidate_list,l_assignment)
                    if(x>res_b):
                        (res_p,res_b,res_s_assignment,res_l_assignment)=(w,x,y,z)
                    l_assignment.pop()
                    i["visited"]=0
        temp_dict={}
        for i in l_candidate_list:
            temp_str=str(i["days"])
            if i["visited"]==0 and temp_str not in temp_dict:
                temp_dict[temp_str]=1
                temp_check=list(map(lambda x,y:x-y,b_available_slots,i["days"]))
         
                if(min(temp_check)>-1):
                    l_assignment.append(i["actual_id"]);
                    i["visited"]=1
                    (w,x,y,z)=turn_spla(common_len,s_len,l_len-1,common_candidate_list,p_remaining,p_assigned,p_available_slots,s_candidate_list,s_assignment,
                    b_remaining-i["req"],b_assigned+i["req"],temp_check,l_candidate_list,l_assignment)
                    if(x>res_b):
                        (res_p,res_b,res_s_assignment,res_l_assignment)=(w,x,y,z)
                    l_assignment.pop()
                    i["visited"]=0
                    
    else:
        s_candidate_slots=[0 for i in range(7)]
        for i in s_candidate_list:
            if i["visited"]==0:              
                s_candidate_slots=list(map(lambda x,y:x+y,s_candidate_slots,i["days"]))
                
        l_candidate_slots=[0 for i in range(7)]
        for i in l_candidate_list:
            if i["visited"]==0:              
                l_candidate_slots=list(map(lambda x,y:x+y,l_candidate_slots,i["days"]))
        res_p,res_s_assignment=spla_alone(s_candidate_slots,s_len,p_remaining,p_assigned,p_available_slots,s_candidate_list,s_assignment,sorted_l,res_b)
        res_b,res_l_assignment=lahsa_alone(l_candidate_slots,l_len,b_remaining,b_assigned,b_available_slots,l_candidate_list,l_assignment,sorted_s,res_p)
                    
    mapper[sorted_s,sorted_l]=(res_p,res_b)
    return (res_p,res_b,res_s_assignment,res_l_assignment)

'''ONLY LAHSA'''
def lahsa_alone(l_candidate_slots,l_len,b_remaining,b_assigned,b_available_slots,l_candidate_list,l_assignment,sorted_s,res_p):
    global mapper
    res_b=b_assigned
    res_l_assignment=l_assignment[:]
    sorted_l=tuple(sorted(l_assignment[:]))

    if (sorted_s,sorted_l) in mapper:
        temp1,temp2=mapper[sorted_s,sorted_l]
        return (temp2,sorted_l)
    
    if(l_len==0):
        mapper[sorted_s,sorted_l]=(res_p,res_b)
        return (res_b,res_l_assignment)
                    
    else:
        temp_lis=list(map(lambda x,y:x-y,b_available_slots,l_candidate_slots))
        if min(temp_lis)>-1:
            res_b+=sum(l_candidate_slots) 
            temp_assign=[]
            for i in l_candidate_list:
                if i["visited"]==0:              
                    temp_assign.append(i["actual_id"])
            temp_assign=l_assignment+temp_assign
            return res_b,temp_assign

        else:
            temp_dict={}
            for i in l_candidate_list:
                temp_str=str(i["days"])
                if i["visited"]==0 and temp_str not in temp_dict:
                    temp_dict[temp_str]=1
                    temp_check=list(map(lambda x,y:x-y,b_available_slots,i["days"]))
                    if(min(temp_check)>-1):
                        i["visited"]=1
                        l_assignment.append(i["actual_id"]);
                        temp_l_slots=list(map(lambda x,y:x-y,l_candidate_slots,i["days"]))
                        (w,x)=lahsa_alone(temp_l_slots,l_len-1,b_remaining-i["req"],b_assigned+i["req"],temp_check,l_candidate_list,l_assignment,sorted_s,res_p)
                        if(w>res_b):
                                (res_b,res_l_assignment)=(w,x)
                        l_assignment.pop()
                        i["visited"]=0
    if (sorted_s,sorted_l) not in mapper:
        mapper[sorted_s,sorted_l]=(res_p,res_b)
    return (res_b,res_l_assignment)


#start=time.time()
(b,b_available_slots,p,p_available_slots,l,l_list,s,s_list,a,a_list,s_candidate_list,l_candidate_list,common_candidate_list,b_remaining,p_remaining, s_candidate_slots, l_candidate_slots) = parse_input()
mapper={}
p_assigned=p-p_remaining
b_assigned=b-b_remaining

common_len=len(common_candidate_list)
s_len=len(s_candidate_list)
l_len=len(l_candidate_list)
    
yel,ley=min_max(common_len,s_len,l_len,common_candidate_list,p_remaining,p_assigned,p_available_slots,s_candidate_list,[],b_remaining,b_assigned,b_available_slots,l_candidate_list,[])
#print(yel,ley)
#Writing to a file
op=open("output.txt","w+")
op.write(str(ley))
op.write("\n")
op.close()
#end=time.time()
#print(end-start)
