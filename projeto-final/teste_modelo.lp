\ Model modelo_pdjt
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  aresta_0_1_0 + aresta_1_1_0 + aresta_2_0_0
   + 1.414213562373095 aresta_2_1_0 + aresta_2_2_0 + aresta_2_3_0
   + aresta_3_1_0 + local_inicio_3_0 + 1000 pedido_no_banco_1
Subject To
 nao_forma_loop_0_0: aresta_0_0_0 = 0
 nao_forma_loop_1_0: aresta_1_1_0 = 0
 nao_forma_loop_2_0: aresta_2_2_0 = 0
 nao_forma_loop_3_0: aresta_3_3_0 = 0
 pickup_visitado_ou_banco_1: aresta_1_0_0 + aresta_1_1_0 + aresta_1_2_0
   + aresta_1_3_0 + pedido_no_banco_1 = 1
 pickup_delivery_0_1: - aresta_0_2_0 + aresta_1_0_0 + aresta_1_1_0
   + aresta_1_3_0 - aresta_2_2_0 - aresta_3_2_0 = 0
 inicio_fim_pt_1_0: aresta_0_1_0 + aresta_0_3_0 = 1
 inicio_fim_pt_2_0: aresta_0_3_0 + aresta_2_3_0 = 1
 caminho_conexo_1_0: aresta_0_1_0 - aresta_1_0_0 - aresta_1_2_0
   - aresta_1_3_0 + aresta_2_1_0 + aresta_3_1_0 = 0
 caminho_conexo_2_0: aresta_0_2_0 + aresta_1_2_0 - aresta_2_0_0
   - aresta_2_1_0 - aresta_2_3_0 + aresta_3_2_0 = 0
 define_local_ini_pt_1_0_0_0: 999999 aresta_0_0_0 <= 999999
 define_local_ini_pt_1_0_1_0: 999999 aresta_0_1_0 + local_inicio_0_0
   - local_inicio_1_0 <= 999997
 define_local_ini_pt_1_0_2_0: 999999 aresta_0_2_0 + local_inicio_0_0
   - local_inicio_2_0 <= 999995
 define_local_ini_pt_1_0_3_0: 999999 aresta_0_3_0 + local_inicio_0_0
   - local_inicio_3_0 <= 999999
 define_local_ini_pt_1_1_0_0: 999999 aresta_1_0_0 - local_inicio_0_0
   + local_inicio_1_0 <= 999991
 define_local_ini_pt_1_1_1_0: 999999 aresta_1_1_0 <= 999994
 define_local_ini_pt_1_1_2_0: 999999 aresta_1_2_0 + local_inicio_1_0
   - local_inicio_2_0 <= 999990
 define_local_ini_pt_1_1_3_0: 999999 aresta_1_3_0 + local_inicio_1_0
   - local_inicio_3_0 <= 999994
 define_local_ini_pt_1_2_0_0: 999999 aresta_2_0_0 - local_inicio_0_0
   + local_inicio_2_0 <= 999990
 define_local_ini_pt_1_2_1_0: 999999 aresta_2_1_0 - local_inicio_1_0
   + local_inicio_2_0 <= 999991
 define_local_ini_pt_1_2_2_0: 999999 aresta_2_2_0 <= 999994
 define_local_ini_pt_1_2_3_0: 999999 aresta_2_3_0 + local_inicio_2_0
   - local_inicio_3_0 <= 999994
 define_local_ini_pt_1_3_0_0: 999999 aresta_3_0_0 - local_inicio_0_0
   + local_inicio_3_0 <= 999999
 define_local_ini_pt_1_3_1_0: 999999 aresta_3_1_0 - local_inicio_1_0
   + local_inicio_3_0 <= 999999
 define_local_ini_pt_1_3_2_0: 999999 aresta_3_2_0 - local_inicio_2_0
   + local_inicio_3_0 <= 999999
 define_local_ini_pt_1_3_3_0: 999999 aresta_3_3_0 <= 999999
 ini_servico_0_0_0: - local_inicio_0_0 <= 0
 ini_servico_1_0_0: local_inicio_0_0 <= 240
 ini_servico_0_0_1: - local_inicio_1_0 <= -20
 ini_servico_1_0_1: local_inicio_1_0 <= 100
 ini_servico_0_0_2: - local_inicio_2_0 <= -10
 ini_servico_1_0_2: local_inicio_2_0 <= 100
 ini_servico_0_0_3: - local_inicio_3_0 <= 0
 ini_servico_1_0_3: local_inicio_3_0 <= 240
 pickup_antes_delivery_1_0: local_inicio_1_0 - local_inicio_2_0 <= 0
 define_ub_correto_pt_10_0_0: 999999 aresta_0_0_0 <= 999999
 define_ub_correto_pt_10_0_1: 999999 aresta_0_1_0 + ub_apos_servico0_0
   - ub_apos_servico1_0 <= 999977
 define_ub_correto_pt_10_0_2: 999999 aresta_0_2_0 + ub_apos_servico0_0
   - ub_apos_servico2_0 <= 1.000021e+06
 define_ub_correto_pt_10_0_3: 999999 aresta_0_3_0 + ub_apos_servico0_0
   - ub_apos_servico3_0 <= 999999
 define_ub_correto_pt_10_1_0: 999999 aresta_1_0_0 - ub_apos_servico0_0
   + ub_apos_servico1_0 <= 999999
 define_ub_correto_pt_10_1_1: 999999 aresta_1_1_0 <= 999977
 define_ub_correto_pt_10_1_2: 999999 aresta_1_2_0 + ub_apos_servico1_0
   - ub_apos_servico2_0 <= 1.000021e+06
 define_ub_correto_pt_10_1_3: 999999 aresta_1_3_0 + ub_apos_servico1_0
   - ub_apos_servico3_0 <= 999999
 define_ub_correto_pt_10_2_0: 999999 aresta_2_0_0 - ub_apos_servico0_0
   + ub_apos_servico2_0 <= 999999
 define_ub_correto_pt_10_2_1: 999999 aresta_2_1_0 - ub_apos_servico1_0
   + ub_apos_servico2_0 <= 999977
 define_ub_correto_pt_10_2_2: 999999 aresta_2_2_0 <= 1.000021e+06
 define_ub_correto_pt_10_2_3: 999999 aresta_2_3_0 + ub_apos_servico2_0
   - ub_apos_servico3_0 <= 999999
 define_ub_correto_pt_10_3_0: 999999 aresta_3_0_0 - ub_apos_servico0_0
   + ub_apos_servico3_0 <= 999999
 define_ub_correto_pt_10_3_1: 999999 aresta_3_1_0 - ub_apos_servico1_0
   + ub_apos_servico3_0 <= 999977
 define_ub_correto_pt_10_3_2: 999999 aresta_3_2_0 - ub_apos_servico2_0
   + ub_apos_servico3_0 <= 1.000021e+06
 define_ub_correto_pt_10_3_3: 999999 aresta_3_3_0 <= 999999
 ub_correto_pt_2_0_0: ub_apos_servico0_0 <= 300
 ub_correto_pt_2_0_1: ub_apos_servico1_0 <= 300
 ub_correto_pt_2_0_2: ub_apos_servico2_0 <= 300
 ub_correto_pt_2_0_3: ub_apos_servico3_0 <= 300
 ini_fim_demanda_0_0: ub_apos_servico0_0 = 0
 ini_fim_demanda_1_0: ub_apos_servico3_0 = 0
Bounds
 aresta_0_0_0 <= 1
 aresta_0_1_0 <= 1
 aresta_0_2_0 <= 1
 aresta_0_3_0 <= 1
 aresta_1_0_0 <= 1
 aresta_1_1_0 <= 1
 aresta_1_2_0 <= 1
 aresta_1_3_0 <= 1
 aresta_2_0_0 <= 1
 aresta_2_1_0 <= 1
 aresta_2_2_0 <= 1
 aresta_2_3_0 <= 1
 aresta_3_0_0 <= 1
 aresta_3_1_0 <= 1
 aresta_3_2_0 <= 1
 aresta_3_3_0 <= 1
 pedido_no_banco_1 <= 1
End
