from datetime import datetime, timedelta

class Treino:
    def __init__(self,id,data,distancia,tempo):
        self.set_id(id) #só um underline
        self.set_data(data)
        self.set_distancia(distancia)
        self.set_tempo(tempo)

    def set_id(self,id):
        if id <= 0:
            raise ValueError("O ID deve ser um número positivo.")
        self.__id=id

    def set_data(self, data):
        try:
            self.__data = datetime.strptime(data, "%d/%m/%Y")
        except (TypeError, ValueError):
            raise ValueError("A data deve estar no formato dd/mm/aaaa.")

    def set_distancia(self,distancia):
        if distancia <= 0:
            raise ValueError("A distância deve ser um número positivo.")
        self.__distancia=distancia

    def set_tempo(self,tempo):
        if tempo <= timedelta(0):
            raise ValueError("O tempo deve ser um número positivo.")
        self.__tempo=tempo


    def get_id(self): return self.__id
    def get_data(self):return self.__data
    def get_distancia(self): return self.__distancia
    def get_tempo(self): return self.__tempo

    def Pace(self):
        if self.__distancia <= 0:
            raise ValueError("A distância deve ser maior que zero.")

        segundos_por_km = self.__tempo.total_seconds() / self.__distancia
        return timedelta(seconds=segundos_por_km)    
    
    def __str__(self):
        data_formatada = self.__data.strftime("%d/%m/%Y")
        return (
            f"ID: {self.__id}\n"
            f"Data: {data_formatada}\n"
            f"Distância percorrida: {self.__distancia}\n"
            f"Tempo: {self.__tempo}"
        )
class TreinoUI:
    treinos=[]

    @staticmethod
    def Menu():
        print(f"1-Inserir novo treino\n2-Listar todos os treinos\n3-Listar treino por ID\n4-Atualizar treino\n5-Excluir\n6-Mais rápido\n7-Sair")
        return int(input("Escolha uma opção: "))

    @staticmethod
    def main():
        op=0
        while op != 7:
            op=TreinoUI.Menu()
            if op == 1:TreinoUI.Inserir()
            if op == 2:TreinoUI.Listar()
            if op == 3:TreinoUI.Listar_Id()
            if op == 4:TreinoUI.Atualizar()
            if op == 5:TreinoUI.Excluir()
            if op == 6:TreinoUI.MaisRapido()

    @classmethod
    def Inserir(cls):
        id=int(input("Informe o ID: "))
        data=input("Informe a data (dd/mm/aaaa): ")
        datetime.strptime(data,"%d/%m/%Y")
        distancia=float(input("Informe a distância: "))
        tempo=timedelta(seconds=int(input("Informe o tempo (segundos): ")))

        x=Treino(id,data,distancia,tempo)
        cls.treinos.append(x)
        pass

    @classmethod
    def Listar(cls):
        for x in cls.treinos:
            print(x)

    @classmethod
    def Listar_Id(self):
        try:
            id_treino=int(input("Informe o ID do treino: "))
            treino=TreinoUI.buscar(id_treino)
            if treino is None: print("Treino não encontrado")
            else: print(treino)
        except ValueError: print("ID inválido")
            
    @staticmethod
    def buscar(id):
        for treino in TreinoUI.treinos:
            if treino.get_id()==id:
                return treino
        return None

    @classmethod
    def Atualizar(cls):
        try:
            id_treino=int(input("Informe o ID do treino: "))
            treino=TreinoUI.buscar(id_treino)

            if treino is None: 
                print("Treino não encontrado")
                return
        
            data=input("Informe a nova data (dd/mm/aaaa): ")
            datetime.strptime(data,"%d/%m/%Y")
            distancia=float(input("Informe a nova distância: "))
            tempo=timedelta(seconds=int(input("Informe o novo tempo (segundos): ")))

            treino.set_data(data)
            treino.set_distancia(distancia)
            treino.set_tempo(tempo)
            print("Treino atualizado")
        
        except ValueError: print("Dados inválidos")
        pass

    @classmethod
    def Excluir(cls):
        try:
            id_treino=int(input("Informe o ID do treino: "))
            treino=TreinoUI.buscar(id_treino)

            if treino is None: 
                print("Treino não encontrado")
                return

            cls.treinos.remove(treino)
            print("Treino excluido")
        except ValueError:
            print("Id inválido")

    @classmethod
    def MaisRapido(cls):
        if not cls.treinos:
            print("Nenhum treino cadastrado")
            return

        treino_mais_rapido = cls.treinos[0]

        for treino in cls.treinos[1:]:
            pace_atual = treino.get_tempo().total_seconds() / treino.get_distancia()
            pace_mais_rapido = (
                treino_mais_rapido.get_tempo().total_seconds()
                / treino_mais_rapido.get_distancia()
            )

            if pace_atual < pace_mais_rapido:
                treino_mais_rapido = treino

        print("Treino mais rápido:")
        print(treino_mais_rapido)
        pace = treino_mais_rapido.Pace()
        minutos, segundos = divmod(int(pace.total_seconds()), 60)
        print(f"Pace: {minutos}:{segundos:02d} min/km")

TreinoUI.main()