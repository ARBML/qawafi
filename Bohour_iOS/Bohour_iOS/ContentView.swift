//
//  ContentView.swift
//  Bohour_iOS
//
//  Created by Omar on 06/05/2022.
//

import SwiftUI

struct ContentView: View {
    
    @State var firstPart = "الشطر الأول \nالشطر الثاني \n..."
    @State var response:ResponseNew? = nil
    @State var isloading = false
    @State var errorMessage = ""
    var placeholderText = "الشطر الأول \nالشطر الثاني \n..."
    @State var numOfBayts = 0
    @State var aboutShown = false
    @State var disableButton = false
    
    var body: some View {
        VStack{
            HStack{
                Image(systemName: "info.circle")
                    .font(.system(size: 20))
                    .padding()
                    .opacity(0)
                Spacer()
                Image("qawafi")
                    .resizable()
                    .frame(width: 80, height: 80)
                    .padding(-16)
                Spacer()
                Image(systemName: "info.circle")
                    .font(.system(size: 20))
                    .foregroundColor(.myPrimary)
                    .padding()
                    .onTapGesture {
                        aboutShown = true
                    }
            }
            if !errorMessage.isEmpty {
                Text(errorMessage)
                    .font(.system(size: 12))
                    .foregroundColor(.red)
                    .frame(maxWidth:.infinity)
                    .padding(12)
                    .background(Color.red.opacity(0.2))
                    .cornerRadius(8)
                    .padding(.horizontal)

            }
            VStack(alignment:.leading){
                Text("اكتب قصيدة لتحليلها")
                    .font(.system(size: 32, weight: .bold))
                    .padding(.bottom,4)
                Text("اكتب نص القصيدة وافصل كل شطر في سطر جديد")
                    .foregroundColor(Color.gray_6)
                    .padding(.bottom,12)
                ZStack(alignment:.bottomTrailing){
                    //editor
                    TextEditor(text: $firstPart)
                        .frame(height:200)
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
                Spacer()
                Button {
                    
                    if !isButtonEnabled() {
                        return
                    }
                    
                    //1. check form
                    if firstPart.count < 10  {
                        withAnimation {
                            errorMessage = "الرجاء التأكد من كتابة بيتي شعر"
                        }
                        return
                    }
                    
                    //2. no errors
                    errorMessage = ""
                    
                    
                    //3. start loading
                    isloading = true
                    disableButton = true
                    
                    
                    //4. call api
                    Task{
                        do{
                            if let response = try? await API.getAnalysis(firstPart) {
                                //5. show results
                                Timer.scheduledTimer(withTimeInterval: 0.5, repeats: false) { timer in
                                    isloading = false
                                    disableButton = false
                                    self.response = response
                                    
                                }
                                

                            }else{
                                withAnimation {
                                    errorMessage = "الرجاء التأكد من كتابة أبيات صحيحة"
                                }
                                isloading = false
                                disableButton = false
                                Timer.scheduledTimer(withTimeInterval:2, repeats: false) { timer in
                                    withAnimation {
                                        errorMessage = ""
                                    }
                                }
                                
                            }
                        }
                    }
                    
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
            .padding(32)
        }
        .sheet(item: $response) {
        } content: { response in
            ResultsView(response: response)
                .environment(\.layoutDirection, .rightToLeft)
                .environment(\.locale,.init(identifier: "ar"))
                .preferredColorScheme(.light)
        }
        .sheet(isPresented: $aboutShown, content: {
            AboutView()
                .environment(\.layoutDirection, .rightToLeft)
                .environment(\.locale,.init(identifier: "ar"))
                .preferredColorScheme(.light)
        })
        .onAppear {}
        .onChange(of: firstPart) { newValue in
            numOfBayts = firstPart.split(separator: "\n").count / 2
        }
    }
    
    func isButtonEnabled() -> Bool {
        return firstPart != placeholderText &&
        firstPart.count >= 20 &&
        numOfBayts != 0 &&
        !disableButton
    }
    
    func getBody(_ text:String) -> String {
        return String(text.trimmingCharacters(in: .whitespacesAndNewlines))
    }
    
    func getArrayOfParts(_ text:String) -> [String]{
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
        
        return body
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
