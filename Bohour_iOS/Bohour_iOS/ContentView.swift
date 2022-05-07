//
//  ContentView.swift
//  Bohour_iOS
//
//  Created by Omar on 06/05/2022.
//

import SwiftUI

struct ContentView: View {
    
    @State var firstPart = ""
    @State var secondPart = ""
    @State var response:Response? = nil
    @State var isloading = false
    @State var errorMessage = ""
    
    var body: some View {
        NavigationView{
            VStack(alignment:.leading){
                Text("اكتب بيت شعر مكون من شطرين لتحليله ")
                    .foregroundColor(Color.gray_6)
                TextField("الشطر الأول", text: $firstPart)
                    .modifier(TextFieldModifier())
                TextField("الشطر الثاني", text: $secondPart)
                    .modifier(TextFieldModifier())
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
                    
                    //1. check form
                    if firstPart.count < 10 || secondPart.count < 10 {
                        errorMessage = "الرجاء التأكد من كتابة بيتي شعر"
                        return
                    }
                    
                    //2. no errors
                    errorMessage = ""
                    
                    
                    //3. start loading
                    isloading = true
                    
                    //4. call api
                    Task{
                        do{
                            if let response = try? await API.getResults(part_1: firstPart, part_2: secondPart) {
                                //5. show results
                                Timer.scheduledTimer(withTimeInterval: 0.5, repeats: false) { timer in
                                    isloading = false
                                    self.response = response
                                }
                                
                            }else{
                                errorMessage = "الرجاء التأكد من الانترنت"
                            }
                        }
                    }
                    
                } label: {
                    Group{
                        if isloading {
                            LoadingView()
                        }else{
                            Text("تحليل البيت").bold()
                        }
                    }
                    .frame(minHeight:54)
                    .frame(maxWidth:.infinity)
                    .background(Color.myPrimary)
                    .foregroundColor(.white)
                    .cornerRadius(8)
                }
            }
            .padding()
            .navigationTitle("حلّل بيت شعر")
            //.background(Color.myLight)
        }
        .sheet(item: $response) {
            
        } content: { response in
            ResultsView(firstPart: response.name, secondPart: response.job)
        }


    }
}

struct ResultsView : View {
    
    var firstPart:String = "قفا نبك من ذكرى حبيب ومنزل"
    var secondPart:String = "بسقط اللوى بين الدخول فحومل"
    @State private var showDetails = false
    
    var body : some View {
        VStack(alignment:.leading){
            Text("\(firstPart)\n\(secondPart)")
                .font(.system(size: 18, weight: .bold))
                .multilineTextAlignment(.center)
                .foregroundColor(Color.myLight)
                .lineSpacing(10)
                .frame(maxWidth:.infinity)
                .padding()
            if showDetails {
                VStack{
                    Text("البحر")
                    Text("الطويل")
                        .font(.system(size: 24, weight: .black))
                        .bold()
                        .frame(maxWidth:.infinity)
                        .foregroundColor(Color.myPrimary)
                }
                .opacity(showDetails ?  1 : 0)
                .padding(24)
                .background(Color.myLight)
                .cornerRadius(8)
                .transition(.scale)
            }
            Spacer()
        }
        .padding()
        .background(Color.myPrimary)
        .onAppear {
            Timer.scheduledTimer(withTimeInterval: 0.1, repeats: false) { _ in
                withAnimation {
                    showDetails = true
                }
            }
        }
    }
}

struct TextFieldModifier: ViewModifier {
    func body(content: Content) -> some View {
        content
            .padding()
            .cornerRadius(8)
            .font(.system(size: 18))
            .accentColor(Color.myPrimary)
            .overlay{
                RoundedRectangle(cornerRadius: 8)
                    .stroke(Color.gray_1, lineWidth: 1)
            }
            .background(
                Color.white
                    .cornerRadius(8)
                    .shadow(color: Color.gray_1, radius: 10, x: 0, y: 10)
            )
            

    }
}

struct LoadingView : View {
    
    @State var activeIndex = 0
    let numRects = 6
    var color = Color.white
    
    var body : some View {
        HStack{
            ForEach(0..<numRects){i in
                RoundedRectangle(cornerRadius: 2)
                    .foregroundColor(i == activeIndex ? Color.myLight : Color.myLight.opacity(0.5))
                    .frame(width:12,height:8)
                    .scaleEffect(i == activeIndex ? 1.5 : 1)
                    .padding(.leading, i == 3 ? 8 : 0)
            }
        }
        .onAppear {
            Timer.scheduledTimer(withTimeInterval: 0.2, repeats: true) { timer in
                
                withAnimation(.spring()){
                    activeIndex += 1
                    
                    if activeIndex == numRects {
                        activeIndex = 0
                    }
                }
            }
        }
    }
}

extension Color {
    
    //grays
    static let gray_1 = Color(red: 0.95, green: 0.95, blue: 0.95)
    static let gray_2 = Color(red: 0.90, green: 0.90, blue: 0.90)
    static let gray_3 = Color(red: 0.80, green: 0.80, blue: 0.80)
    static let gray_4 = Color(red: 0.70, green: 0.70, blue: 0.70)
    static let gray_5 = Color(red: 0.60, green: 0.60, blue: 0.60)
    static let gray_6 = Color(red: 0.50, green: 0.50, blue: 0.50)
    
    //selected pallete
    static let myPallete = pallete_1
    
    //pallete colors
    static let myPrimary = myPallete["primary"]!
    static let mySecondary = myPallete["secondary"]!
    static let myDark = myPallete["dark"]!
    static let myLight = myPallete["light"]!
    
    //all color palletes
    static let pallete_1 = ["primary":Color(hex: "417D7A"),
                     "secondary":Color(hex: "1D5C63"),
                     "dark":Color(hex: "1A3C40"),
                     "light":Color(hex: "EDE6DB")]
}

extension Color {
    init(hex: String) {
        let hex = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var int: UInt64 = 0
        Scanner(string: hex).scanHexInt64(&int)
        let a, r, g, b: UInt64
        switch hex.count {
        case 3: // RGB (12-bit)
            (a, r, g, b) = (255, (int >> 8) * 17, (int >> 4 & 0xF) * 17, (int & 0xF) * 17)
        case 6: // RGB (24-bit)
            (a, r, g, b) = (255, int >> 16, int >> 8 & 0xFF, int & 0xFF)
        case 8: // ARGB (32-bit)
            (a, r, g, b) = (int >> 24, int >> 16 & 0xFF, int >> 8 & 0xFF, int & 0xFF)
        default:
            (a, r, g, b) = (1, 1, 1, 0)
        }

        self.init(
            .sRGB,
            red: Double(r) / 255,
            green: Double(g) / 255,
            blue:  Double(b) / 255,
            opacity: Double(a) / 255
        )
    }
}


struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        Group{
            ContentView()
            ResultsView()
            LoadingView()
                .preferredColorScheme(.dark)
        }
        .environment(\.layoutDirection, .rightToLeft)
        .environment(\.locale,.init(identifier: "ar"))
        
    }
}
