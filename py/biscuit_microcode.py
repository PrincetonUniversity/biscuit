# Helper functions for generating microcode in verilog for bit_proc

# Generate a number of identical lines in microcode
# n_lines = # of lines
# signal = instruction being microcoded
# cp0_wen = bool
# pc_mux_sel = {x, next, branch}
# a_mux_sel = {reg, pc}
# a_addr = {x, r[abc]}
#

# Microcoding Guide:
#  Each call counts as one micro-op, the number of repeat is ADDITIONAL executions
#  Last line must always have a new pc_mux_sel and last_uop

def gen_lines (uop_idx, repeat_cnt, signal, cp0_wen, csr_rw, pc_mux_sel, a_mux_sel, a_rd_tmp, a_seq_en, a_offset, a_acc_dir, b_seq_en, b_offset, b_acc_dir, a_addr, b_addr, wb_addr, mem_acc, wb_en, wb_addr_en, inc_subw_en, wb_data_en, a_use_temp_reg, b_imm_used, b_imm_type, b_imm_en, b_imm_sel, b_imm_zero, addsub_fn, carry_in, logic_fn, mul_fn, adj_sel, adj_en, wb_off_sel, fn_type, fl_en, addr_dir, addr_en, br_reg_en, new_inst):
    
    out = "assign " + signal + "[" + str(uop_idx) + "] = { "
    
    # Sometimes intermediate micro-ops not needed depending on subword size
    # Having a negative repeat count should indicate how many are neede.
    if repeat_cnt < 0:
        return uop_idx

    #handle indications on shift

    repeat_cnt = str(int(repeat_cnt))
    if repeat_cnt == 'regshift':
        out += 'rep_reg, 5\'d0, '
    elif repeat_cnt == 'immshift':
        out += 'rep_imm, 5\'d0, '
    else:
        #Assume it's a constant number
        out += 'rep_const, 5\'d' + repeat_cnt + ', '
        
    out += 'y, ' if  cp0_wen else 'n, '
    out += 'csr_' + csr_rw + ', '
    out += 'pc_' + pc_mux_sel + ', '
    out += 'am_' + a_mux_sel + ', '
    out += 'y, ' if a_rd_tmp else 'n, '
    out += 'rf_' + a_seq_en + ', '
    out += '5\'d' + str(a_offset) +', '
    out += 'dir_'+a_acc_dir +', '
    out += 'rf_' + b_seq_en + ', '
    out += '5\'d' + str(b_offset) +', '
    out += 'dir_'+b_acc_dir +', '
    out += 'addr_x, ' if a_addr == 'x' else a_addr + ', '
    out += 'addr_x, ' if b_addr == 'x' else b_addr + ', '
    out += 'addr_x, ' if wb_addr == 'x' else wb_addr + ', '
    out += 'y, ' if  mem_acc else 'n, '
    out += 'y, ' if  wb_en else 'n, '

    out += 'y, ' if wb_addr_en else 'n, ' 
    out += 'y, ' if inc_subw_en else 'n, '
    out += 'y, ' if wb_data_en else 'n, ' 

    out += 'y, ' if a_use_temp_reg else 'n, '

# Handle immediates:
#   b_imm_reg_en
    out += 'y, ' if b_imm_en else 'n, '
#   b_imm_reg_sel
    out += 'b_imm_x, ' if b_imm_sel == 'x' else 'b_imm_' + b_imm_sel + ', '
#   b_imm_type
    out += 'immed_type_' + b_imm_type + ', '
#   b_imm_zero override
    out += 'y, ' if b_imm_zero else 'n, '


    out += 'bm_imm, ' if b_imm_used == 'imm' else 'shift_lsb_Xhl, ' if b_imm_used == 'shift_lsb' else 'bm_reg, '

    out += 'fn_sub, ' if addsub_fn == 'sub' else 'fn_add, '
    out += 'carry_prop, ' if carry_in == 'prop' else 'carry_msb, ' if carry_in == 'msb' else 'carry_in_1, ' if carry_in == '1' else 'carry_in_0, '
    out += 'fn_xor, ' if logic_fn == 'xor' else 'fn_or, ' if logic_fn == 'or' else 'fn_a_nb, ' if logic_fn == 'a_nb' else 'fn_and, '
 
    out += 'adj_' + adj_sel + ', '
    out += 'y, ' if adj_en else 'n, '
    out += 'y, ' if wb_off_sel == 'subw' else 'n, '

    out += 'fn_type_'
    out += (fn_type +', ') if (fn_type == 'arith' or fn_type == 'logic' or fn_type == 'shift' or fn_type == 'jalr' or fn_type == 'mul') else 'x, '

    out += 'mul_'+ mul_fn + ', '
    out += 'y, ' if fl_en else 'n, '
    out += 'shift_left, ' if addr_dir == "left" else 'shift_right, '
    out += 'y, ' if addr_en else 'n, '
    out += 'y, ' if br_reg_en else 'n, '
    out += 'y' if new_inst else 'n'
    out += '};'

    print(out)

    return uop_idx + 1
