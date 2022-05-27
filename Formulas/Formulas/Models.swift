//
//  Models.swift
//  Formulas
//
//  Created by Omar on 14/05/2022.
//

import Foundation

class Formula {
    var name:String = ""
    var a:Double = 0.0
    func evaluate(){}
    
    init(name:String, a:Double, @escaping evaluate:()->()){
        
    }
}
