//
//  ResultView.swift
//  Bohour_iOS
//
//  Created by Omar on 25/05/2022.
//

import SwiftUI

struct ResultsView : View {
    
    var response:Response
    @State private var showDetails = true
    private let innerSpacing = 8.0
    @State var selectedBait:BaitsAnalysis
    @Namespace var firstPartId
    let osoor = ["الجاهلي", "الإسلامي", "الأموي", "العباسي", "العثماني", "الحديث"]
    
    var body : some View {
        
        VStack(alignment:.leading, spacing: 24){
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
                            Text(response.meter)
                                .font(.system(size: 36, weight: .black))
                                .bold()
                                .frame(maxWidth:.infinity)
                                .foregroundColor(Color.myDark)
                                .padding(.top,12)
                        }
                        .modifier(BoxModifier())
                        .opacity(showDetails ?  1 : 0)
                        .transition(.scale)
                        
                    }
                    
                    Rectangle()
                        .frame(height: 1)
                        .foregroundColor(Color.myLight)
                        .padding(.horizontal)
                    
                    //second row
                    
                    HStack(spacing:innerSpacing){
                        //qafiyah
                        VStack{
                            Text("القافية")
                            Text(response.qafiah.type)
                                .font(.system(size: 24, weight: .bold))
                                .frame(maxWidth:.infinity)
                                .foregroundColor(Color.myDark)
                        }
                        .modifier(BoxModifier())
                        .opacity(showDetails ?  1 : 0)
                        .transition(.scale)
                        
                        //topic
                        VStack{
                            Text("الموضوع")
                            Text(response.topic[0].name)
                                .font(.system(size: 24, weight: .bold))
                                .frame(maxWidth:.infinity)
                                .foregroundColor(Color.myDark)
                        }
                        .modifier(BoxModifier())
                        .opacity(showDetails ?  1 : 0)
                        .transition(.scale)
                        
                    }
                    
                    Rectangle()
                        .frame(height: 1)
                        .foregroundColor(Color.myLight)
                        .padding(.horizontal)
                    
                    //era
                    VStack{
                        Text("العصر")
                        ScrollView(.horizontal){
                            HStack{
                                ForEach(osoor,id:\.self){ asr in
                                    Text(asr)
                                        .padding(8)
                                        .background(asr == response.era[0].name ? Color.myPrimary : Color.myLight)
                                        .cornerRadius(8)
                                        .foregroundColor(asr == response.era[0].name ? Color.myLight : Color.myDark)
                                        .opacity(asr == response.era[0].name ? 1 : 0.4)
                                }
                            }
                        }
                    }
                    .opacity(showDetails ?  1 : 0)
                    .transition(.scale)
                    .padding()
                    
                }
                .background(Color.white)
                .cornerRadius(12)
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
                
                ScrollView{
                    VStack{
                        ForEach(response.baits_analysis){ bayt in
                            VStack(alignment: .leading){
                                ScrollViewReader { p in
                                    ScrollView(.horizontal){
                                        HStack{
                                            PartView(partIndex: 0, selectedBait: bayt)
                                                .padding(.leading)
                                                .id(firstPartId)
                                            PartView(partIndex: 1, selectedBait: bayt)
                                        }
                                    }
                                    .onAppear {
                                        p.scrollTo(firstPartId)
                                    }
                                }
                                .padding(.bottom,12)
                            }
                        }
                    }
                }
                
                //abyat
                
//                ScrollView {
//
//                    VStack{
//                        ForEach(response.baits_analysis){ bayt in
//                            VStack(spacing:innerSpacing){
//                                HStack{
//                                    Text("\(String(bayt.bait_diacritized.split(separator: "#")[0]))")
//                                        .opacity(showDetails ?  1 : 0)
//                                        .transition(.scale)
//                                    Spacer()
//                                }
//                                HStack{
//                                    Spacer()
//                                    Text("\(String(bayt.bait_diacritized.split(separator: "#")[1]))")
//                                        .opacity(showDetails ?  1 : 0)
//                                        .transition(.scale)
//                                }
//                            }
//                            .modifier(BoxModifier())
//                            .font(.system(size: 18, weight: .bold))
//                            .foregroundColor(Color.myPrimary)
//                        }
//
//                    }
//
//                }
                
                
            }

            
            
            //bayte
//            Text("\(response.baitsAnalysis[0].baitDiacritized)")
//                .font(.system(size: 18, weight: .bold))
//                .multilineTextAlignment(.center)
//                .foregroundColor(Color.myLight)
//                .lineSpacing(10)
//                .frame(maxWidth:.infinity)
//                .padding()
        }
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

func getPart(_ partIndex:Int,  _ str:String) -> String {
    let parts = str.split(separator: "#")
    let part = String(parts[partIndex]).trimmingCharacters(in: .whitespacesAndNewlines)
    return part
}

struct PartView : View {
    
    var partIndex:Int
    var selectedBait:BaitsAnalysis
    
    var body : some View {
        VStack(alignment:.leading){
            Text(getPart(partIndex, selectedBait.bait_diacritized))
                .font(.system(size: 24))
                .bold()
                .padding(.bottom,8)
            VStack(alignment:.leading){
                //)parts
                HStack(spacing:1){
                    ForEach(Array(getPart(partIndex, selectedBait.arudi_style)), id:\.self){ c in
                        Text(String(c))
                            .frame(width:10)
                            .font(.system(size: 12))
                    }
                }
                
                HStack(spacing:1){
                    ForEach(Array(getPart(partIndex, selectedBait.tafeelat_pattern)), id:\.self){ c in
                        Circle()
                            .frame(width:10, height:8)
                            .foregroundColor(c == "1" ? Color.myPrimary : Color.myLight)
                            .opacity(c == " " ? 0 : 1)
                            .cornerRadius(4)
                    }
                }
                
                // failatun
                
                
            }
        }
        .padding()
        .background(Color.white)
        .cornerRadius(12)
    }
}

struct ResultsView_Previews: PreviewProvider {
    static var previews: some View {
        ResultsView(response: Response.getSample()!, selectedBait: Response.getSample()!.baits_analysis[0])
            .environment(\.layoutDirection, .rightToLeft)
            .environment(\.locale,.init(identifier: "ar"))
    }
}
