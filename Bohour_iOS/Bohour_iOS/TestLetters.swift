//
//  File.swift
//  Bohour_iOS
//
//  Created by Omar on 25/05/2022.
//

import SwiftUI

struct TestLetters : View {
    
    let string : String = "قفا نبك من ذكرى حبيب ومنزل"
    @State var stringParts : String = "قفانبكمنذكرىحبيبنومنزلي"
    @State var parts = "11010 1101010 11010 110110"
    
    let highlight : String = "نبك ومنزل حومل"
    
    var body : some View {
        VStack{
            //word
//            HStack(spacing:2){
//                ForEach(string.components(separatedBy: " "), id:\.self){ word in
//                    if highlight.components(separatedBy: " ").contains(word) {
//                        Text(word)
//                            .bold()
//                            .padding(2)
//                            .background(Color.myLight)
//                            .cornerRadius(4)
//
//                    }else{
//                        Text(word)
//                    }
//                }
//            }
            Text(string).bold()
            VStack(alignment:.leading){
                //)parts
                HStack(spacing:1){
                    ForEach(Array(stringParts), id:\.self){ c in
                        Text(String(c))
                            .frame(width:8)
                            .font(.system(size: 10))
                    }
                }
                
                HStack(spacing:1){
                    ForEach(Array(parts), id:\.self){ c in
                        Circle()
                            .frame(width:8, height:8)
                            .foregroundColor(c == "1" ? Color.myPrimary : Color.myLight)
                            .opacity(c == " " ? 0 : 1)
                            .cornerRadius(4)
                    }
                }
            }
            .padding()
            .background(Color.white)
            .cornerRadius(8)
            .shadow(color: Color.gray_1, radius: 10, x: 0, y: 8)
        }
        .onAppear {
            
            var parts_spaced:[Int] = []
            
            //get space
            for (i,c) in parts.enumerated() {
                if String(c) == " " {
                    parts_spaced.append(i)
                }
            }
            
            // insert in orignal string
            for i in parts_spaced {
                let idx = stringParts.index(stringParts.startIndex,offsetBy: i)
                stringParts.insert(" ", at: idx)
            }
            
                
                
        }
    }
}

struct TestLetters_Previews: PreviewProvider {
    static var previews: some View {
        TestLetters()
            .environment(\.layoutDirection, .rightToLeft)
            .environment(\.locale,.init(identifier: "ar"))
    }
}

