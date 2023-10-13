from db_handler import *
import enum

cpu_procent = 0.25
gpu_procent = 0.40
motherboard_procent = 0.15
psd_procent = 0.06
ps_procent = 0.04
ram_procent = 0.05

power = 0


def parametr_select(column, cpu_list):
    parametr_list = []
    for cpu in cpu_list:
        parametr_list.append(cpu[column])
    return parametr_list


class select_alg(list):

    def select_cpu(self):  # Выбор CPU по параметрам из уже отобранных по цене

        cpu_list = [0] * len(self)

        tp_list = parametr_select(1, self)
        cpu_list[tp_list.index(max(tp_list))] += 3

        canals_list = parametr_select(2, self)
        cpu_list[canals_list.index(max(canals_list))] += 2

        cores_list = parametr_select(3, self)
        cpu_list[cores_list.index(max(cores_list))] += 2

        freq_list = parametr_select(4, self)
        cpu_list[freq_list.index(max(freq_list))] += 3

        cache_list = parametr_select(5, self)
        cpu_list[cache_list.index(max(cache_list))] += 1

        tdp_list = parametr_select(6, self)
        cpu_list[tdp_list.index(min(tdp_list))] += 2

        ramt_list = parametr_select(9, self)
        cpu_list[ramt_list.index(max(ramt_list))] += 2

        ramc_list = parametr_select(10, self)
        cpu_list[ramc_list.index(max(ramc_list))] += 2

        ramf_list = parametr_select(11, self)
        cpu_list[ramf_list.index(max(ramf_list))] += 2

        video_core_list = parametr_select(7, self)
        for i, el in enumerate(video_core_list):
            if bool(i):
                cpu_list[i] += 1

        if cpu_list.count(max(cpu_list)) != 1:
            price_list = parametr_select(12, self)
            cpu_list[price_list.index(min(price_list))] += 10

        return self[cpu_list.index(max(cpu_list))]

    def select_gpu(self):  # Выбор GPU по параметрам уже отобранных по цене

        check = [0] * len(self)
        column = 2
        max_param = 0

        while column <= 3:
            for p in range(len(self)):
                if self[p][column] > max_param:
                    max_param = self[p][column]

            for cpu_n in range(len(self)):
                if max_param in self[cpu_n]:
                    check[cpu_n] += 1
            column += 1

        while column <= 5:
            max_param = 10 ** 9
            for p in range(len(self)):
                if self[p][column] < max_param:
                    max_param = self[p][column]

            for cpu_n in range(len(self)):
                if max_param in self[cpu_n]:
                    check[cpu_n] += 1
            column += 1

        return self[check.index(max(check))]

    def select_ram(self):  # Выбор RAM по параметрам из уже отобранных по цене

        ram_list = [0] * len(self)

        ramm_list = parametr_select(1, self)
        ram_list[ramm_list.index(max(ramm_list))] += 3

        ramt_list = parametr_select(2, self)
        ram_list[ramt_list.index(max(ramt_list))] += 2

        ramc_list = parametr_select(3, self)
        ram_list[ramc_list.index(max(ramc_list))] += 2

        ramf_list = parametr_select(4, self)
        ram_list[ramf_list.index(max(ramf_list))] += 2

        if ram_list.count(max(ram_list)) != 1:
            price_list = parametr_select(5, self)
            ram_list[price_list.index(min(price_list))] += 10

        return self[ram_list.index(max(ram_list))]

    def select_psd(self):  # Выбор PSD по параметрам из уже отобранных по цене

        check = [0] * len(self)
        max_param = 0
        column = 2

        for p in range(len(self)):
            if self[p][column] > max_param:
                max_param = self[p][column]

        for cpu_n in range(len(self)):
            if max_param in self[cpu_n]:
                check[cpu_n] += 1
        column += 1

        while column <= 4:
            max_param = 10 ** 9
            for p in range(len(self)):
                if self[p][column] < max_param:
                    max_param = self[p][column]

            for cpu_n in range(len(self)):
                if max_param in self[cpu_n]:
                    check[cpu_n] += 1
            column += 1

        return self[check.index(max(check))]

    def select_mb(self):  # Выбор материнской платы по параметрам из уже отобранных по цене

        mb_list = [0] * len(self)

        chipset_list = parametr_select(1, self)
        mb_list[chipset_list.index(max(chipset_list))] += 3

        ramt_list = parametr_select(3, self)
        mb_list[ramt_list.index(max(ramt_list))] += 2

        sata_list = parametr_select(5, self)
        mb_list[sata_list.index(max(sata_list))] += 1

        satav_list = parametr_select(6, self)
        mb_list[satav_list.index(max(satav_list))] += 2

        m2_list = parametr_select(7, self)
        mb_list[m2_list.index(max(m2_list))] += 2

        usb32_list = parametr_select(8, self)
        mb_list[usb32_list.index(max(usb32_list))] += 1

        usb20_list = parametr_select(9, self)
        mb_list[usb20_list.index(max(usb20_list))] += 1

        if mb_list.count(max(mb_list)) != 1:
            price_list = parametr_select(5, self)
            mb_list[price_list.index(min(price_list))] += 10

        return self[mb_list.index(max(mb_list))]

    def select_ps(self):  # Выбор блока питания по параметрам из уже отобранных по цене

        check = [0] * len(self)
        column = 2

        while column <= 3:
            max_param = 10 ** 9
            for p in range(len(self)):
                if self[p][column] < max_param:
                    max_param = self[p][column]

            for cpu_n in range(len(self)):
                if max_param in self[cpu_n]:
                    check[cpu_n] += 1
            column += 1

        return self[check.index(max(check))]


class db_search(float):  # Отбор из БД необходимых данных
    power = 0

    def search_cpu(price_pc):  # Отбор из БД CPU
        global power
        price_max = int(price_pc * (cpu_procent + 0.05))
        price_min = int(price_pc * (cpu_procent - 0.05))

        cpu_selection = db_sel("cpu", price_max, price_min)

        try:
            if len(cpu_selection) > 1:
                result = select_alg.select_cpu(cpu_selection)
            else:
                result = cpu_selection[0]
            power += result[6]
        except IndexError:
            result = ["Нет комплектующей", 0]

        return result

    def search_motherboard(cpu, price_pc):  # Отбор из БД материнской платы
        global power
        from db_handler import mb_db
        price_max = int(price_pc * (motherboard_procent + 0.05))
        price_min = int(price_pc * (motherboard_procent - 0.05))

        mb_sel = mb_db(cpu, price_max, price_min)

        try:
            if len(mb_sel) > 1:
                result = select_alg.select_mb(mb_sel)
            else:
                result = mb_sel[0]
        except IndexError:
            result = ["Нет комплектующей", 0]

        return result

    def search_gpu(price_pc):  # Отбор из БД GPU
        global power
        from db_handler import db_sel
        price_max = int(price_pc * (gpu_procent + 0.05))
        price_min = int(price_pc * (gpu_procent - 0.05))

        gpu_selection = db_sel("gpu", price_max, price_min)

        try:
            if len(gpu_selection) > 1:
                result = select_alg.select_gpu(gpu_selection)

            else:
                result = gpu_selection[0]
            power += result[4]
        except IndexError:
            result = ["Нет комплектующей", 0]

        return result

    def search_psd(price_pc):  # Отбор из БД PSD
        global power
        from db_handler import db_sel
        psd_price_max = int(price_pc * (psd_procent + 0.05))
        psd_price_min = int(price_pc * (psd_procent - 0.05))

        psd_selection = db_sel("psd", psd_price_max, psd_price_min)

        try:
            if len(psd_selection) > 1:
                result = select_alg.select_psd(psd_selection)
            else:
                result = psd_selection[0]
            power += result[3]
        except IndexError:
            result = ["Нет комплектующей", 0]

        return result

    def search_ram(price_pc):  # Отбор из БД RAM
        global power
        from db_handler import db_sel
        price_max = int(price_pc * (ram_procent + 0.05))
        price_min = int(price_pc * (ram_procent - 0.05))

        ram_selection = db_sel("ram", price_max, price_min)

        try:
            if len(ram_selection) > 1:
                result = select_alg.select_ram(ram_selection)
            else:
                result = ram_selection[0]
        except IndexError:
            result = ["Нет комплектующей", 0]

        return result

    def search_ps(price_pc):  # Отбор из БД блока питания
        global power
        from db_handler import ps_db
        price_max = int(price_pc * (ps_procent + 0.05))
        price_min = int(price_pc * (ps_procent - 0.05))

        ps_selection = ps_db(power, price_max, price_min)

        try:
            if len(ps_selection) > 1:
                result = select_alg.select_ps(ps_selection)
            else:
                result = ps_selection[0]
        except IndexError:
            result = ["Нет комплектующей", 0]

        return result


def pc_selection(price_pc):  # Сборка данных в один список (конечный список комплектующих для ПК)
    cpu = db_search.search_cpu(price_pc)
    motherboard = db_search.search_motherboard(cpu, price_pc)
    gpu = db_search.search_gpu(price_pc)
    ram = db_search.search_ram(price_pc)
    psd = db_search.search_psd(price_pc)
    ps = db_search.search_ps(price_pc)

    pc_list = [cpu, motherboard, gpu, ram, psd, ps]
    return pc_list
