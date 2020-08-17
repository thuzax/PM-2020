from numpy import round

class Vertice:

    def __init__(self, idx, coord_x,coord_y,demanda,ini_janela,fim_janela,   
                    duracao_servico,par_pickup, par_delivery):
        
        self.idx = idx 
        self.coord_x = coord_x 
        self.coord_y = coord_y 
        self.demanda = demanda 
        self.ini_janela = ini_janela 
        self.fim_janela = fim_janela 
        self.duracao_servico = duracao_servico 
        self.par_pickup = par_pickup 
        self.par_delivery = par_delivery 

        self.e_pickup = True if self.demanda > 0 else False
        self.e_delivery = True if self.demanda < 0 else False
        
        self.e_deposito = not(self.e_pickup and self.e_delivery)



    def retorna_par(self):
        if (self.e_pickup):
            return self.par_pickup
        return self.par_delivery


    def get_string(self):
        texto = ""
        texto = "id: "
        texto += str(self.idx)
        texto += ", "
        texto += "coord_x: "
        texto += str(round(self.coord_x, 2))
        texto += ", "
        texto += "coord_y: "
        texto += str(round(self.coord_y, 2))
        texto += ", "
        texto += "dem: "
        texto += str(self.demanda)
        texto += ", "
        texto += "ini_jan: "
        texto += str(self.ini_janela)
        texto += ", "
        texto += "fim_jan: "
        texto += str(self.fim_janela)
        texto += ", "
        texto += "durac: "
        texto += str(self.duracao_servico)
        texto += ", "
        texto += "par_p: "
        texto += str(self.par_pickup)
        texto += ", "
        texto += "par_d: "
        texto += str(self.par_delivery)
        texto += ", "
        texto += "e_pick: "
        texto += str(self.e_pickup)
        texto += ", "
        texto += "e_delivery: "
        texto += str(self.e_delivery)
        texto += ", "
        texto += "e_deposito: "
        texto += str(self.e_deposito)

        return texto