//
//  ContentView.swift
//  Bohour_iOS
//
//  Created by Omar on 06/05/2022.
//

import SwiftUI

struct ContentView: View {
    
    @StateObject var previousItems = PreviousResults()
        
    @State var firstPart = "الشطر الأول \nالشطر الثاني \n..."
    @State var response:ResponseNew? = nil
    @State var isloading = false
    @State var errorMessage = ""
    var placeholderText = "الشطر الأول \nالشطر الثاني \n..."
    @State var numOfBayts = 0
    @State var aboutShown = false
    @State var disableButton = false
    @State var introViewShown = false
    let launchedBefore = UserDefaults.standard.bool(forKey: "launchedBefore")
    @FocusState private var nameIsFocused: Bool
    @State var showHistory = false
    
    var body: some View {
        ZStack(alignment:.top){
            HStack{
                Button {
                    showHistory = true
                } label: {
                    Image(systemName: "clock.arrow.circlepath")
                        .font(.system(size: 20))
                        .padding()
                        .foregroundColor(.myPrimary)
                        .opacity(previousItems.items.count > 0 ? 1.0 : 0.0)
                }

                Spacer()
                Image("qawafi")
                    .resizable()
                    .frame(width: 80, height: 80)
                    .padding(-16)
                    .onTapGesture {
                        aboutShown = true
                    }
                Spacer()
                Image(systemName: "info.circle")
                    .font(.system(size: 20))
                    .foregroundColor(.myPrimary)
                    .padding()
                    .opacity(0)
            }
            VStack{
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
                        .font(.system(size: 28, weight: .black))
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
                            .focused($nameIsFocused)
                            .onTapGesture {
                                if firstPart == placeholderText {
                                    firstPart = ""
                                }
                            }
                        //counter
                        HStack{
                            Button {
                                let pb: UIPasteboard = UIPasteboard.general
                                firstPart = pb.string ?? ""
                            } label: {
                                Label("لصق", systemImage: "doc.on.clipboard")
                                    .foregroundColor(.myPrimary)
                                    .padding(.horizontal,8)
                            }
                            
                            Button {
                                firstPart = ""
                            } label: {
                                Label("مسح", systemImage: "trash")
                                    .foregroundColor(firstPart.count == 0 || firstPart == placeholderText ? .white : .red.opacity(0.7))
                                    .padding(.horizontal,8)
                            }

                            Spacer()
                            Text("عدد الأبيات \(numOfBayts)")
                                .foregroundColor(numOfBayts == 0 ? Color.gray_3 : Color.myDark)
                            
                        }
                        .padding()
                    }
                    Spacer()
                    Text("جاري تحليل الأبيات ...")
                        .opacity(isloading ? 1 : 0)
                        .foregroundColor(.myPrimary)
                        .frame(maxWidth:.infinity)
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
                        nameIsFocused = false
                        
                        
                        //4. call api
                        Task{
                            do{
                                if let response = try? await API.getAnalysis(firstPart) {
                                    
                                    //5. show results
                                    Timer.scheduledTimer(withTimeInterval: 0.5, repeats: false) { timer in
                                        isloading = false
                                        disableButton = false
                                        
                                        //add to history and show
                                        self.previousItems.items.append(response)
                                        self.response = response
                                        
                                    }
                                    

                                }else{
                                    withAnimation {
                                        errorMessage = "الرجاء التأكد من كتابة أبيات صحيحة"
                                    }
                                    isloading = false
                                    disableButton = false
                                    nameIsFocused = true
                                    Timer.scheduledTimer(withTimeInterval:3, repeats: false) { timer in
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
                        .modifier(ButtonModifier())
                        .opacity(isButtonEnabled() ? 1 : 0.5 )
                    }
                }
                .padding(.horizontal, 32)
            }
            .padding(.top,72)
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
            .sheet(isPresented: $introViewShown, content: {
                IntroView()
                    .environment(\.layoutDirection, .rightToLeft)
                    .environment(\.locale,.init(identifier: "ar"))
                    .preferredColorScheme(.light)
            })
            .sheet(isPresented: $showHistory, content: {
                HistoryView(previousItems: previousItems)
                    .environment(\.layoutDirection, .rightToLeft)
                    .environment(\.locale,.init(identifier: "ar"))
                    .preferredColorScheme(.light)
            })
            .onAppear {
                
                //first launch
                if !launchedBefore  {
                    //show first one
                    Timer.scheduledTimer(withTimeInterval: 0.1, repeats: false) { timer in
                        withAnimation(Animation.spring()) {
                            introViewShown = true
                        }
                    }
                    UserDefaults.standard.set(true, forKey: "launchedBefore")
                }
            }
            .onChange(of: firstPart) { newValue in
                numOfBayts = firstPart.split(separator: "\n").count / 2
                firstPart = firstPart.replacingOccurrences(of: "\n\n", with: "\n")
            }

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
