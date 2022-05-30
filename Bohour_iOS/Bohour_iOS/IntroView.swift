//
//  Intro.swift
//  Bohour_iOS
//
//  Created by Omar Hammad on 5/28/22.
//

import SwiftUI

struct IntroView: View {
    
    @Environment(\.presentationMode) var presentationMode
    @State var showContent = Array(repeating: false, count: 3)
    
    var body: some View {
        VStack{
            //close
            Capsule()
                .frame(width: 50, height: 10)
                .foregroundColor(Color.gray_1)
                .padding(.top)
            //content
            ZStack(alignment: .bottom){
                ScrollView{
                    VStack(alignment: .leading, spacing: 16){
                        Image("qawafi")
                            .resizable()
                            .frame(width: 120, height: 120)
                            .padding(-20)
                        Text("مرحباً بك في قوافي")
                            .font(.system(size: 28, weight: .black))
                        Text("يمكّنك تطبيق قوافي من تحليل قصيدة أو بيت أو مجموعة أبيات من الشعر العربي، من تأليفك أو من القصائد المشهورة")
                            .font(.title3)
                        
                        Feature(image: Image(systemName: "music.note.list"), title: "بحر القصيدة", desc: "تعرف على البحر من قائمة  من ١٥ بحر من بحور الشعر العربي كما صنفها علماء اللغة ")
                            .opacity(showContent[0] ? 1 : 0)
                        
                        Feature(image: Image(systemName: "square.fill.text.grid.1x2"), title: "القافية والروي", desc: "تعرف على قافية القصيدة من وصل أو ردف أو غيرها وعلى حرف روي الأبيات ")
                            .opacity(showContent[1] ? 1 : 0)

                        
                        Feature(image: Image(systemName: "text.redaction"), title: "عيوب الوزن", desc: "تعرف على العيوب من كسر وزحاف وغيرها لكل بيت من أبيات القصيدة")
                            .opacity(showContent[2] ? 1 : 0)
                        
                        Spacer()
                    }
                    .padding(.top,16)
                }
                
                Button {
                    self.presentationMode.wrappedValue.dismiss()
                } label: {
                    Text("ابدأ بكتابة أول قصيدة")
                        .modifier(ButtonModifier())
                }
            }
            .frame(maxHeight:.infinity)
        .padding(.horizontal, 32)
        }
        .onAppear{
            
            // Animation
            let delay = 0.2
            for i in 0..<showContent.count {
                Timer.scheduledTimer(withTimeInterval: delay + Double(i)*delay, repeats: false) { _ in
                    withAnimation {
                        showContent[i] = true
                    }
                }
            }
            
        }

    }
}

struct Intro_Previews: PreviewProvider {
    static var previews: some View {
        IntroView()
            .environment(\.layoutDirection, .rightToLeft)
    }
}

struct Feature: View {
    
    var image:Image
    var title:String
    var desc:String
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack{
                image
                    .font(.title)
                    .foregroundColor(.myPrimary)
                    .environment(\.layoutDirection, .leftToRight)
                Text(title)
                    .font(.title2)
                    .bold()
                    .frame(maxWidth:.infinity, alignment: .leading)
            }
            Text(desc)
        }
        .padding(20)
        .background(Color.myLight.opacity(0.5))
        .cornerRadius(16)
    }
}
