//
//  ResultView.swift
//  Bohour_iOS
//
//  Created by Omar on 25/05/2022.
//

import SwiftUI

struct ResultsView : View {
    
    var response:ResponseNew
    @State private var showDetails = true
    private let innerSpacing = 8.0
    let osoor = [
"الجاهلي والإسلامي",
        "العباسي",
                    "المملوكي والفاطمي",
        "العثماني والحديث"
    ]
    @State var sha6rz:[String] = []
    @State var tafeelat = ""
    @State var showContent = Array(repeating: false, count: 10)
    
    func isAsr(_ asr:String) -> Bool{
        switch response.era[0] {
        case "العصر الجاهلي":
            return asr == osoor[0]
        case "العصر العباسي":
            return asr == osoor[1]
        case "العصر الفاطمي":
            return asr == osoor[2]
        case "العصر الحديث":
            return asr == osoor[3]
        default:
            return false
        }
    }
    
    var body : some View {
        
        VStack(alignment:.center, spacing: 24){
            
            //close
            Capsule()
                .frame(width: 50, height: 10)
                .foregroundColor(Color.mySecondary)
                .padding(.top)

            
            ScrollView{
                //Top section
                VStack(alignment:.leading){
                    Text("تحليل القصيدة")
                        .font(.system(size: 24))
                        .bold()
                        .foregroundColor(Color.myLight)
                        .padding(.horizontal)
                    //top box
                    VStack(spacing:innerSpacing){
                        HStack(spacing:innerSpacing){
                            //bahr
                            VStack{
                                Group{
                                    Text("بحر ") + Text(response.meter)
                                }
                                .font(.system(size: 28, weight: .black))
                                .foregroundColor(Color.myDark)
                                .padding(.top,12)
                                    
                            }
                            .padding(20)
                            .opacity(showDetails ?  1 : 0)
                            .transition(.scale)
                            
                        }
                        
                        Text("قصيدة بحرف الروي: \(response.qafiyah[0])")
                            .padding(.top,-8)
                            .padding(.bottom)
                        
                        Rectangle()
                            .frame(height: 1)
                            .foregroundColor(Color.myLight)
                            .padding(.horizontal)
                        
                        //second row
                        
                        HStack(spacing:innerSpacing){
                            //qafiyah
                            VStack{
                                Text("القافية")
                                Text(getQafiyahString(response.qafiyah))
                                    .font(.system(size: 24, weight: .bold))
                                    .frame(maxWidth:.infinity)
                                    .foregroundColor(Color.myDark)
                                    .minimumScaleFactor(0.8)
                            }
                            .padding(20)
                            .opacity(showDetails ?  1 : 0)
                            .transition(.scale)
                            
                            
                            //topic
                            VStack{
                                Text("الموضوع")
                                Text(response.theme[0].split(separator: " ")[1])
                                    .font(.system(size: 24, weight: .bold))
                                    .frame(maxWidth:.infinity)
                                    .foregroundColor(Color.myDark)
                            }
                            .padding(20)
                            .opacity(showDetails ?  1 : 0)
                            .transition(.scale)
                            
                        }
                        
                        Rectangle()
                            .frame(height: 1)
                            .foregroundColor(Color.myLight)
                            .padding(.horizontal)
                        
                        //era
                        VStack{
                            Text("أقرب لقصائد العصر")
                            ScrollView(.horizontal){
                                HStack{
                                    ForEach(osoor,id:\.self){ asr in
                                        Text(asr)
                                            .padding(8)
                                            .background(isAsr(asr) ? Color.myPrimary : Color.myLight)
                                            .cornerRadius(8)
                                            .foregroundColor(isAsr(asr) ? Color.myLight : Color.myDark)
                                            .opacity(isAsr(asr) ? 1 : 0.4)
                                    }
                                }
                            }
                        }
                        .opacity(showDetails ?  1 : 0)
                        .transition(.scale)
                        .padding()
                        
                    }
                    .background(Color.white)
                    .cornerRadius(16)
                    .opacity(showContent[0] ? 1 : 0)
                }
                .padding()
                
                //Bottom section
                VStack(alignment:.leading){
                    
                    //title
                    Text("تحليل الأبيات")
                        .font(.system(size: 24))
                        .bold()
                        .foregroundColor(Color.myLight)
                        .padding(.horizontal)
                    
                    //analysis
                    
                    VStack{
                        ForEach(0..<sha6rz.count, id:\.self){ i in
                            HStack{
                                if (i % 2 != 0){
                                    Spacer()
                                }
                                PartView(bait_diacritized: sha6rz[i], arudi_style: response.arudi_style[i][0], tafeelat_pattern: response.arudi_style[i][1], tafeelatWord: getPart(i % 2, getTafeelatWord(response.closest_patterns[0][2])))
                                if (i % 2 == 0){
                                    Spacer()
                                }
                            }
                            .opacity(showContent[i < sha6rz.count ? i : 0] ? 1 : 0)
                        }
                    }
                    .padding(.horizontal)
                    
                    
            }
            }
            
        }
        .background(Color.myPrimary)
        .onAppear {
            
            // Animation
            let delay = 0.2
            for i in 0..<showContent.count {
                Timer.scheduledTimer(withTimeInterval: delay + Double(i)*delay, repeats: false) { _ in
                    withAnimation {
                        showContent[i] = true
                    }
                }
            }
            
            //SHA6rz
            for b in response.diacritized {
                let bayteParts = b.split(separator: "#")
                for part in bayteParts {
                    sha6rz.append(String(part).trimmingCharacters(in: .whitespacesAndNewlines))
                }
            }
            
            //tafeelat
            switch response.closest_patterns[0][2] {
            case .string(let name):
                tafeelat = name.replacingOccurrences(of: "#", with: " ")
            case .double(_):
                print("number")
            }
            
            print(response.qafiyah[1])
            print(response.era[0])
            
        }
    }
    
    func getTafeelatWord(_ ptr:ClosestPattern) -> String{
        switch ptr {
        case .string(let name):
            return name
        case .double(_):
            print("number")
            return ""
        }
    }
    
    func getQafiyahString(_ qfyz:[String]) -> String{
        return qfyz[1..<qfyz.count].joined(separator: ",")
    }

}

func getPart(_ partIndex:Int,  _ str:String) -> String {
    let parts = str.split(separator: "#")
    let part = String(parts[partIndex]).trimmingCharacters(in: .whitespacesAndNewlines)
    return part
}

struct PartView : View {
    
    var bait_diacritized:String
    var arudi_style:String
    var tafeelat_pattern:String
    var tafeelatWord:String
    @State var tafeelatSpaced = ""
        
    var body : some View {
        VStack(alignment:.leading, spacing: 8){
            Text(bait_diacritized)
                .font(.system(size: 24))
                .bold()
            Text(tafeelatWord)
                .font(.system(size: 20))
                .foregroundColor(.mySecondary)
            
            VStack(alignment:.leading){
                //)parts
                HStack(spacing:1){
                    ForEach(Array(arudi_style), id:\.self){ c in
                        Text(String(c))
                            .frame(width:10)
                            .font(.system(size: 12))
                    }
                }
                
                HStack(spacing:1){
                    ForEach(Array(tafeelatSpaced), id:\.self){ c in
                        Circle()
                            .frame(width:10, height:8)
                            .foregroundColor(c == "1" ? Color.myPrimary : Color.myLight)
                            .opacity(c == " " ? 0 : 1)
                            .cornerRadius(4)
                    }
                }
                
                
            }
        }
        .padding()
        .background(Color.white)
        .cornerRadius(12)
        .onAppear{
            
            addSpacesToPattern()
            
        }
    }
    
    func addSpacesToPattern(){
        var spaceIndecies:[Int] = []
        for i in 0..<arudi_style.count{
            if arudi_style[i] == " " {
                spaceIndecies.append(i)
            }
        }
        tafeelatSpaced = tafeelat_pattern
        for i in spaceIndecies {
            tafeelatSpaced.insert(" ", at: tafeelatSpaced.index(tafeelatSpaced.startIndex, offsetBy: i))
        }
    }
}

struct ResultsView_Previews: PreviewProvider {
    static var previews: some View {
        ResultsView(response: ResponseNew.getSample()!)
            .environment(\.layoutDirection, .rightToLeft)
            .environment(\.locale,.init(identifier: "ar"))
    }
}
