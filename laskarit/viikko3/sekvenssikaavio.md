sequenceDiagram
    participant main
    participant Machine
    participant Engine
    participant FuelTank

    main ->>+ Machine : Machine()
    Machine ->> FuelTank : FuelTank()
    Machine ->> FuelTank : fill(40)
    Machine ->> Engine : Engine(self._tank)
    Machine -->>- main : 

    main ->>+ Machine : drive()
    Machine ->>+ Engine : start()
    
    Engine ->>+ FuelTank : consume(5)
    Engine ->>- Machine : 
    Machine ->>+ Engine : is_running()
    Engine -->>- Machine : True

    Machine ->>+ Engine : use_energy()
    Engine ->>+ FuelTank : consume(10)
    Engine ->>- Machine : 
    Machine ->>- main : 
