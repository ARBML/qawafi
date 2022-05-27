//
//  ContentView.swift
//  Bohour_iOS
//
//  Created by Omar on 06/05/2022.
//

import SwiftUI

struct ContentView: View {
    
    @State var firstPart = "الشطر الأول \nالشطر الثاني \n..."
    @State var response:Response? = nil
    @State var isloading = false
    @State var errorMessage = ""
    var placeholderText = "الشطر الأول \nالشطر الثاني \n..."
    @State var numOfBayts = 0
    
    var body: some View {
        VStack{
            Image("qawafi")
                .resizable()
                .frame(width: 80, height: 80)
                .padding(-16)
            VStack(alignment:.leading){
                Spacer()
                Text("اكتب قصيدة لتحليلها")
                    .font(.system(size: 32, weight: .bold))
                    .padding(.bottom,4)
                Text("اكتب نص القصيدة وافصل كل شطر في سطر جديد")
                    .foregroundColor(Color.gray_6)
                    .padding(.bottom,12)
                ZStack(alignment:.bottomTrailing){
                    //editor
                    TextEditor(text: $firstPart)
                        .frame(height:240)
                        .font(.system(size: 24))
                        .modifier(TextFieldModifier())
                        .foregroundColor(firstPart == placeholderText ? Color.gray_3 : Color.myDark)
                        .lineSpacing(8)
                        .onTapGesture {
                            if firstPart == placeholderText {
                                firstPart = ""
                            }
                        }
                    //counter
                    Text("عدد الأبيات \(numOfBayts)")
                        .padding()
                        .foregroundColor(Color.myPrimary)
                }
                if !errorMessage.isEmpty {
                    Text(errorMessage)
                        .font(.system(size: 12))
                        .foregroundColor(.red)
                        .frame(maxWidth:.infinity)
                        .padding(12)
                        .background(Color.red.opacity(0.2))
                        .cornerRadius(8)
                }
                Spacer()
                Button {
                    
                    if !isButtonEnabled() {
                        return
                    }
                    
                    //1. check form
                    if firstPart.count < 10  {
                        errorMessage = "الرجاء التأكد من كتابة بيتي شعر"
                        return
                    }
                    
                    //2. no errors
                    errorMessage = ""
                    
                    
                    //3. start loading
                    isloading = true
                    
                    //4.prep input
                    let body = getArrayOfParts(firstPart)
                    
                    self.response = Response.getSample()
                    
                    //5. call api
//                    Task{
//                        do{
//                            if let response = try? await API.getResults(part_1: firstPart, part_2: "") {
//                                //5. show results
//                                Timer.scheduledTimer(withTimeInterval: 0.5, repeats: false) { timer in
//                                    isloading = false
//                                    self.response = response
//                                }
//
//                            }else{
//                                errorMessage = "الرجاء التأكد من الاتصال بالانترنت"
//                                isloading = false
//                            }
//                        }
//                    }
                    
                } label: {
                    Group{
                        if isloading {
                            LoadingView()
                        }else{
                            Text("تحليل القصيدة").bold()
                        }
                    }
                    .disabled(!isButtonEnabled())
                    .frame(minHeight:54)
                    .frame(maxWidth:.infinity)
                    .background(Color.myPrimary)
                    .foregroundColor(.white)
                    .cornerRadius(8)
                    .opacity(isButtonEnabled() ? 1 : 0.5 )
                }
            }
            .padding()
        }
        .sheet(item: $response) {
        } content: { response in
            ResultsView(response: response, selectedBait: response.baits_analysis[0])
                .environment(\.layoutDirection, .rightToLeft)
                .environment(\.locale,.init(identifier: "ar"))
                .preferredColorScheme(.light)
        }
        .onAppear {
            //load json
            if let data = readLocalFile(forName: "anlss") {
                let res = parse(jsonData: data)
                self.response = response
                print("loaded")
            }else{
                print("not loaded")
            }
            
            //link num bayts to first name
            
        }
        .onChange(of: firstPart) { newValue in
            numOfBayts = firstPart.split(separator: "\n").count / 2
        }
    }
    
    func isButtonEnabled() -> Bool {
        return firstPart != placeholderText &&
        firstPart.count >= 20 &&
        numOfBayts != 0
    }
    
    func getArrayOfParts(_ text:String){
        let parts = text.split(separator: "\n")
        var body:[String] = []
        var tempBait = ""
        var partIndex = 0
        
        for p in parts {
            if partIndex == 0 {
                tempBait = String(p)
                partIndex += 1
            }else{
                tempBait += " # " + String(p)
                body.append(tempBait)
                partIndex = 0
            }
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        Group{
            ContentView()
//            ResultsView()
//            LoadingView()
//                .preferredColorScheme(.dark)
//            TestLetters()
        }
        .environment(\.layoutDirection, .rightToLeft)
        .environment(\.locale,.init(identifier: "ar"))
        
    }
}
