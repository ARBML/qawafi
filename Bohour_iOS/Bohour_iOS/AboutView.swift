//
//  AboutView.swift
//  Bohour_iOS
//
//  Created by Omar Hammad on 5/27/22.
//

import SwiftUI

struct AboutView: View {
    var body: some View {
        ScrollView{
            VStack(alignment:.leading, spacing:24){
                Image("qawafi")
                    .resizable()
                    .frame(width: 144, height: 144)
                    .padding(-20)
                
                Text("بسم الله الرحمن الرحيم")
                    .font(.title)
                
                Text("فريق قوافي بدأ من ثلاثة باحثين في مجال علوم حاسب، ومحبين للغة العربية وخدمتها، والسعي لترك بصمة تنفع كل محب للغة العربية. يتكون فريقنا من.")
                
                NameView(name: "زيد اليافعي", major: "طالب دكتوراه في علوم الحاسب الآلي", spcial: "تعلم عميق ومعالجة اللغات الطبيعية")
                
                NameView(name: "ماجد الشيباني", major: "طالب ماجستير في علوم الحاسب الآلي", spcial: "تعلم عميق وعلوم اللغة العربية")
                
                NameView(name: "عمر حمّاد", major: "طالب دكتوراه في علوم الحاسب الآلي", spcial: "التفاعل بين الإنسان والحاسب الآلي")
                
                Text("يسعدنا تواصلكم معنا لابداء مقترحاكم لهذا المشروع أو لأي سبب آخر")
                
                Text("جميع الحقوق محفوظة لفريق قوافي 2022")
                    .foregroundColor(.myLight)
            }
            .padding(40)
        }
        
    }
}

struct NameView: View {
    
    let name:String
    let major:String
    let spcial:String
    
    var body: some View {
        VStack(alignment:.leading, spacing: 8){
            Text(name)
                .font(.title)
                .bold()
                .foregroundColor(.myPrimary)
            Group{
                Text(major)
                Text(spcial)
            }
            .font(.system(size: 20))
            .foregroundColor(.gray_6)
            Rectangle()
                .foregroundColor(.myLight)
                .frame(height: 1)
                .padding(.vertical)
        }
    }
}

struct AboutView_Previews: PreviewProvider {
    static var previews: some View {
        AboutView()
            .environment(\.layoutDirection, .rightToLeft)
    }
}
