/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package verifyuser;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.util.ArrayList;

/**
 *
 * @author BAÑON
 */
public class VerifyUser {

    public static void main(String[] args) {
        
        ArrayList<String> lista = new ArrayList<String>();
        lista.add("8168562");//El comercio
        lista.add("66746614");//La republica
        lista.add("9075022");//RPP
        lista.add("158871696");//Municipalidad de Lima
        lista.add("2667501056");//SIT
        lista.add("291870169");//Publimetro peru
        lista.add("65549291");//America noticias        
        lista.add("248692867");//Canal_N
        lista.add("19602540");//Peru 21
        lista.add("2535831924");//Peru 21 Ciudad
        lista.add("85840608");//Diario Correo
        lista.add("125737181");//Trome
        lista.add("376311344");//Exitosa Noticias        
        lista.add("2205328350");//Exitosa Diario
        lista.add("21889656");//Radio Capital
        lista.add("187657372");//Frecuencia Latina        
        lista.add("39620329");//Terra Peru
        lista.add("201246685");//Diario16
        lista.add("110822488");//GestionPE
        lista.add("29330019");//LaMula        
        lista.add("14165101");//Utero PE
        
        try{
            FileInputStream fstream = new FileInputStream("output.csv");
            PrintWriter out = new PrintWriter(new FileWriter("new_output.csv"));
            DataInputStream in = new DataInputStream(fstream);
            BufferedReader br = new BufferedReader(new InputStreamReader(in));
            String strLine = ""; 
            while ((strLine = br.readLine()) != null)   {
                
                String parts[] = strLine.split("\\|");
		String idUsuario = parts[1];
                
                for(String i:lista){
                    if(idUsuario.compareTo(i)==0){                                                
                        strLine = strLine.substring(0,strLine.length()-3)+'2'+strLine.substring(strLine.length()-2);                        
                    }
                }
                
                out.print(strLine);
                out.print("\n");
            }
            
            out.close();
            in.close();
            
        }catch(Exception e){
            
        }

    }
    
}
