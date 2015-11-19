# -*- coding: utf-8 -*-

import GraphDriver;
import networkx as nx;
import Bloc;
import sys
sys.setrecursionlimit(10000);

class CondensedDriver(GraphDriver.GraphDriver):
    
    def get_name():
        return "condensed";
        
    def create_graph(self, instructions_table, vma_instructions_table):
        waiting_list = {};
        i = 0;
        bloc_cur = Bloc.Bloc(instructions_table[i].vma);
        bloc_origin = bloc_cur;
        
        while(i <= len(instructions_table)-1):
            cur_inst = instructions_table[i];
            
            
            if(super(CondensedDriver, self).is_jump(cur_inst)):
                #condition pour faire remonter l'adresse cible d'un jump vers un bloc déjà créé
                if(int(cur_inst.operands[0].ascii, 0)<int(cur_inst.vma,0)):#
                    bloc_cur.addInstruction(cur_inst);
                    bloc_tmp = bloc_origin.getBloc(cur_inst.operands[0].ascii);
                    j=0;
                    print(j);
                    print(bloc_tmp.instruction[j]);
                    Bloc_mid1 = Bloc.Bloc(bloc_tmp.instruction[j].vma);
                    while j<len(bloc_tmp.instruction):
                        Bloc_mid1.addInstruction(bloc_tmp.instruction[j]);
                        j=j+1;
                    bloc_origin.getParent(bloc_tmp).replaceSon(Bloc_mid1, bloc_tmp);
                    print(Bloc_mid1.instructionStr());
                    bloc_cur.addSon(Bloc_mid1);
                    Bloc_mid1.addSon(bloc_tmp.getSon());
                    Bloc_tmp=Bloc.Bloc(instructions_table[i+1]);
                    bloc_cur.addSon(Bloc_tmp);
                    bloc_cur=Bloc_tmp;
                else:
                    bloc_cur.addInstruction(cur_inst);
                    Bloc_tmp=Bloc.Bloc( instructions_table[i]);
                    bloc_cur.addSon(Bloc_tmp);
                    #print(int(cur_inst.operands[0].ascii, 0));
                    waiting_list[int(cur_inst.operands[0].ascii, 0)] = bloc_cur;
                    bloc_cur = Bloc_tmp;
              
            else:
                if(int(cur_inst.vma,0) in waiting_list):
                    #print(waiting_list[int(cur_inst.vma, 0)]);
                    bloc_tmp=Bloc.Bloc(cur_inst);
                    waiting_list[int(cur_inst.vma, 0)].addSon(bloc_tmp);
                    bloc_cur.addSon(bloc_tmp);
                    bloc_cur = bloc_tmp;
                else:
                    bloc_cur.addInstruction(cur_inst);
           
            i = i+1;
        graph = nx.DiGraph();
        #essai avec historique
        historique = [];
        graph = bloc_origin.get_graph(graph);
        
        return graph;




