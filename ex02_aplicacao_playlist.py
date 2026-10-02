from datetime import datetime, timedelta

class PlayList:
    def __init__(self,id,nome,descricao):
        self.set_id(id)
        self.set_nome(nome)
        self.set_descricao(descricao)

    def set_id(self,id):
        if id <= 0: raise ValueError("O ID deve ser maior que zero.")
        self.__id=id
    def set_nome(self,nome):
        if nome == "": raise ValueError("O nome deve ser informado.")
        self.__nome=nome
    def set_descricao(self,descricao):
        if descricao == "": raise ValueError("A descrição deve ser informada.")
        self.__descricao=descricao

    def get_id(self):
        return self.__id
    def get_nome(self):
        return self.__nome
    def get_descricao(self):
        return self.__descricao

    def Tempo_total(self,itens,musicas):
        tempo_total=timedelta()

        for item in itens:
            if item.get_id_playlist() == self.__id:
                musica=next(
                    (musica for musica in musicas
                    if musica.get_id()==item.get_id_musica()),
                    None
                )
                if musica is not None:
                    tempo_total+=musica.get_duracao()
        return tempo_total

    def __str__(self):
        return (f"ID: {self.__id}\nNome: {self.__nome}\nDescrição: {self.__descricao}")

class Musica:
    def __init__(self,id,titulo,artista,album,duracao):
        self.set_id(id)
        self.set_titulo(titulo)
        self.set_artista(artista)
        self.set_album(album)
        self.set_duracao(duracao)

    def set_id(self,id):
        if id <= 0: raise ValueError("O ID deve ser maior que zero.")
        self.__id=id
    def set_titulo(self,titulo):
        if titulo == "": raise ValueError("O título deve ser informado.")
        self.__titulo=titulo
    def set_artista(self,artista):
        if artista == "": raise ValueError("O artista deve ser informado.")
        self.__artista=artista
    def set_album(self,album):
        if album == "": raise ValueError("O álbum deve ser informado.")
        self.__album=album
    def set_duracao(self,duracao):
        try:
            minutos, segundos = map(int, duracao.split(":"))
            if minutos < 0 or segundos < 0 or segundos >= 60:
                raise ValueError
            self.__duracao=timedelta(minutes=minutos, seconds=segundos)
        except(TypeError,ValueError): raise ValueError("A duração está em um formato inválido.")

    def get_id(self):
        return self.__id
    def get_titulo(self):
        return self.__titulo
    def get_artista(self):
        return self.__artista
    def get_album(self):
        return self.__album
    def get_duracao(self):
        return self.__duracao

    def __str__(self):
        total_segundos=int(self.__duracao.total_seconds())
        minutos, segundos=divmod(total_segundos, 60)
        duracao_formatada=f"{minutos}:{segundos:02d}"
        return(f"ID: {self.__id}\nTítulo: {self.__titulo}\nArtista: {self.__artista}\nÁlbum: {self.__album}\nDuração: {duracao_formatada}")

class PlayListItem:
    def __init__(self,id,id_playList,id_musica,data_inclusao,sequencia):
        self.set_id(id)
        self.set_id_playList(id_playList)
        self.set_id_musica(id_musica)
        self.set_data_inclusao(data_inclusao)
        self.set_sequencia(sequencia)

    def set_id(self,id):
        if id <= 0: raise ValueError("O ID deve ser maior que zero.")
        self.__id=id
    def set_id_playList(self,id_playList):
        if id_playList <= 0: raise ValueError("O ID da PlayList deve ser maior que zero.")
        self.__id_playList=id_playList
    def set_id_musica(self,id_musica):
        if id_musica <0: raise ValueError("O ID da música deve ser maior que zero.")
        self.__id_musica=id_musica
    def set_data_inclusao(self,data_inclusao):
        try:
            self.__data_inclusao = datetime.strptime(data_inclusao, "%d/%m/%Y")
        except(TypeError,ValueError): raise ValueError("O formato da data está incorreto")
    def set_sequencia(self,sequencia):
        if sequencia <=0: raise ValueError("A posição da música deve ser maior que zero.")
        self.__sequencia=sequencia

    def get_id(self): return self.__id
    def get_id_playlist(self): return self.__id_playList
    def get_id_musica(self): return self.__id_musica
    def get_data_inclusao(self): return self.__data_inclusao
    def get_sequencia(self): return self.__sequencia

    def __str__(self):
        return(f"ID: {self.__id}\nID da Playlist: {self.__id_playList}\n\
               ID da música: {self.__id_musica}\nData de conclusão: {self.__data_inclusao}\nSequência da música: {self.__sequencia}")

class UI:
    playlists=[]
    musicas=[]
    itens=[]

    @staticmethod
    def Main():
        while True:
            op = UI.Menu()
            if op == 1: UI.Nova_playList()
            elif op == 2: UI.Listar()
            elif op == 3: UI.Nova_musica()
            elif op == 4: UI.Adicionar_musica()
            elif op == 5: UI.Listar_Id()
            elif op == 6: UI.Excluir_musica()
            elif op == 7: UI.Excluir_playList()
            elif op == 8: break
            else: print("Opção inválida.")

    @staticmethod
    def Menu():
        print("1 - Inserir playlist\n2 - Listar playlists\n3 - Cadastrar música\n4 - Adicionar música à playlist\n5 - Procurar playlist\n6 - Excluir música da playlist\n7 - Excluir playlist\n8 - Sair")
        return int(input("Escolha uma opção: "))

    @classmethod
    def Nova_playList(cls):
    #Adicionar playlist
        id = int(input("ID: "))

        if cls.buscar(cls.playlists, id) is not None:
            print("Já existe uma playlist com esse ID.")
            return

        nome = input("Nome: ")
        descricao = input("Descrição: ")

        playlist = PlayList(id, nome, descricao)
        cls.playlists.append(playlist)

    @classmethod
    def Nova_musica(cls):
        id = int(input("ID da música: "))

        if cls.buscar(cls.musicas, id) is not None:
            print("Já existe uma música com esse ID.")
            return

        titulo = input("Título: ")
        artista = input("Artista: ")
        album = input("Álbum: ")
        duracao = input("Duração (minutos:segundos): ")

        musica = Musica(id, titulo, artista, album, duracao)
        cls.musicas.append(musica)
        print("Música cadastrada.")

    @classmethod
    def Adicionar_musica(cls):
        id_playlist = int(input("ID da playlist: "))
        playlist = cls.buscar(cls.playlists, id_playlist)

        if playlist is None:
            print("Playlist não encontrada.")
            return

        id_musica = int(input("ID da música: "))
        musica = cls.buscar(cls.musicas, id_musica)

        if musica is None:
            print("Música não encontrada.")
            return

        id_item = int(input("ID do item da playlist: "))

        if cls.buscar(cls.itens, id_item) is not None:
            print("Já existe um item com esse ID.")
            return

        data = input("Data de inclusão (dd/mm/aaaa): ")
        sequencia = int(input("Posição da música na playlist: "))

        item = PlayListItem(
            id_item, id_playlist, id_musica, data, sequencia
        )
        cls.itens.append(item)
        print("Música adicionada à playlist.") 

    @classmethod
    def Listar(cls):
    #Listar playlists + quantidade de músicas
        if not cls.playlists:
            print("Nenhuma playlist cadastrada.")
            return

        for playlist in cls.playlists:
            print(playlist)
            print(f"Tempo total: {playlist.Tempo_total(cls.itens, cls.musicas)}")
            print()

    @classmethod
    def Listar_Id(cls):
    #Listar playlist + quantidade músicas por ID
        id = int(input("Informe o ID da playlist: "))
        playlist = cls.buscar(cls.playlists, id)

        if playlist is None:
            print("Playlist não encontrada.")
        else:
            print(playlist)
            print(f"Tempo total: {playlist.Tempo_total(cls.itens, cls.musicas)}")
            
    @classmethod
    def buscar(cls,lista,id):
        for objeto in lista:
            if objeto.get_id()==id:
                return objeto
        return None

    @classmethod
    def Excluir_musica(cls):
    #excluir música dentro da playlist
        id_playlist = int(input("ID da playlist: "))
        id_musica = int(input("ID da música que deseja excluir: "))

        playlist = cls.buscar(cls.playlists, id_playlist)
        if playlist is None:
            print("Playlist não encontrada.")
            return

        for item in cls.itens:
            if (
                item.get_id_playlist() == id_playlist
                and item.get_id_musica() == id_musica
            ):
                cls.itens.remove(item)
                print("Música excluída da playlist.")
                return

        print("Essa música não está nessa playlist.")

    @classmethod
    def Excluir_playList(cls):
    #excluir playlist
        id = int(input("ID da playlist que quer excluir: "))
        playlist = cls.buscar(cls.playlists, id)

        if playlist is None:
            print("Playlist não encontrada.")
            return

        cls.playlists.remove(playlist)
        cls.itens = [
            item for item in cls.itens
            if item.get_id_playlist() != id
        ]
        print("Playlist excluída.")

UI.Main()