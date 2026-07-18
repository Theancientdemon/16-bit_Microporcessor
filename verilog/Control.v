/*
    Control Unit
        -> Provides Control signals to Alu and Register bank.
        -> Performs Instruction Fetching.
        -> Decodes Instruction.
        -> Sets respective control signals.
        
        -> 2 stage piplined, Fetch and Execute.
        -> Stalls to avoid hazards.
*/

`timescale 1ps/1ps

module Control_Unit (
    input wire CLK,                     // Clock signal
    input wire RST,                     // Reset signal
    input  wire [15:0] Fetch_input,     // Instruction fetched from memory
    output wire Halted,                 // Halt signal

    // REGISTER BANK Control signals
    output reg W_en_reg,                // Write enable
    output reg Sel_AC,                  // Select A or C Bus(Sel_AC ? C_bus : A_bus)

    output reg [3:0] W_addr,            // Write address
    output reg [3:0] R_addr_A,          // Read address for Bus A
    output reg [3:0] R_addr_B,          // Read address for Bus B
    output reg [3:0] Address_Sel,       // Address selection for Address_bus
    output reg [1:0] Control_PC,        // Control signal for Program Counter

    // ALU control signals
    output reg [3:0] operation,         // Operation Select
    output reg [3:0] Shift_count,       // Count for shift operation
    input wire [2:0] cmp_in,           // Comparator output to check for branching

    // Processor signals
    output reg W_en_mem,                // Write enable signal for memory
    output reg Sel_Din,                 // Select between Data_in and ALU_out
    output reg I_O                      // IO signal

);
    // Internal signals
    localparam PC = 4'd15;
    reg can_fetch;
    reg [15:0] instruction;

    // Decoding Instruction
    wire [3:0] opcode;
    wire [3:0] rd;
    wire [3:0] rs;
    wire [3:0] func;
    assign opcode = instruction[15:12];
    assign rd = instruction[11:8];
    assign rs = instruction[7:4];
    assign func = instruction[3:0];

    // FETCH
        // always for FETCH
        always @(posedge CLK) begin
            if (can_fetch) begin
                instruction <= Fetch_input;
            end else begin
                instruction <= 16'b0;   // Stall for 1 Clock cycle.
            end
        end

        // Drive can_fetch
        always @(opcode) begin
            case (opcode)
                // opcodes for which Data_in is not a instruction but a value.
                4'h9, 4'ha, 4'hb, 4'hc, 4'hd, 4'he, 4'hf : begin
                    can_fetch <= 1'b0;  
                end
                default : begin
                    can_fetch <= 1'b1;
                end
            endcase
        end

        // Drive Halted
        // Halt if instruction is Halt instruction
        assign Halted = (instruction == 16'h000f);

    // Reset Block
    always @(posedge CLK) begin
        if (RST) begin
            can_fetch <= 1'b1;
            instruction <= 16'b0;   // Also Disables Halted.
        end
    end

    // Control Logic
    always @(instruction, cmp_in) begin
        case (opcode)
            4'd0: begin // NOP
                // No operation, do nothing
                // Set all to Zero
                W_en_reg = 1'b0;
                Sel_AC = 1'b0;
                W_addr = 4'b0;
                R_addr_A = 4'b0;
                R_addr_B = 4'b0;
                Address_Sel = PC;
                Control_PC = 2'b10; //PC must increment
                operation = 4'b0;
                Shift_count = 4'b0;
                W_en_mem = 1'b0;
                Sel_Din = 1'b0;
                I_O = 1'b0;
            end
            4'd1: begin // ADD
                // Set operation to ADD and select appropriate values on both buses
                W_en_reg = 1'b1;
                Sel_AC = 1'b1;
                W_addr = rd;
                R_addr_A = rs;
                R_addr_B = func;
                Address_Sel = PC;
                Control_PC = 2'b10;
                operation = 4'b0; // ADD
                Shift_count = 4'b0;
                W_en_mem = 1'b0;
                Sel_Din = 1'b0;
                I_O = 1'b0;
            end
            4'd2: begin // SUB
                // Set operation to SUB and select appropriate values on both buses
                W_en_reg = 1'b1;
                Sel_AC = 1'b1;
                W_addr = rd;
                R_addr_A = rs;
                R_addr_B = func;
                Address_Sel = PC;
                Control_PC = 2'b10;
                operation = 4'd1; // sub'
                Shift_count = 4'b0;
                W_en_mem = 1'b0;
                Sel_Din = 1'b0;
                I_O = 1'b0;
            end
            4'd3: begin // AND
                // Set operation to AND and select appropriate values on both buses
                W_en_reg = 1'b1;
                Sel_AC = 1'b1;
                W_addr = rd;
                R_addr_A = rs;
                R_addr_B = func;
                Address_Sel = PC;
                Control_PC = 2'b10;
                operation = 4'd2; // AND
                Shift_count = 4'b0;
                W_en_mem = 1'b0;
                Sel_Din = 1'b0;
                I_O = 1'b0;
            end
            4'd4: begin // OR
                // Set operation to OR and select appropriate values on both buses
                W_en_reg = 1'b1;
                Sel_AC = 1'b1;
                W_addr = rd;
                R_addr_A = rs;
                R_addr_B = func;
                Address_Sel = PC;
                Control_PC = 2'b10;
                operation = 4'd3; // OR
                Shift_count = 4'b0;
                W_en_mem = 1'b0;
                Sel_Din = 1'b0;
                I_O = 1'b0;
            end
            4'd5: begin // XOR
                // Set operation to XOR and select appropriate values on both buses
                W_en_reg = 1'b1;
                Sel_AC = 1'b1;
                W_addr = rd;
                R_addr_A = rs;
                R_addr_B = func;
                Address_Sel = PC;
                Control_PC = 2'b10;
                operation = 4'd4; // XOR
                Shift_count = 4'b0;
                W_en_mem = 1'b0;
                Sel_Din = 1'b0;
                I_O = 1'b0;
            end
            4'd6: begin // NOT
                // Set operation to NOT and select appropriate values on both buses
                W_en_reg = 1'b1;
                Sel_AC = 1'b1;
                W_addr = rd;
                R_addr_A = rs;
                R_addr_B = func;
                Address_Sel = PC;
                Control_PC = 2'b10;
                operation = 4'd5; // NOT
                Shift_count = 4'b0;
                W_en_mem = 1'b0;
                Sel_Din = 1'b0;
                I_O = 1'b0;
            end
            4'd7: begin // SHIFT
                // Set operation to SHIFT and select appropriate values on both buses
                // Also set the shift count
                case (func)
                    4'd0: begin // SLL
                        W_en_reg = 1'b1;
                        Sel_AC = 1'b1;
                        W_addr = rd;
                        R_addr_A = rd;
                        R_addr_B = 4'd0;
                        Address_Sel = PC;
                        Control_PC = 2'b10;
                        operation = 4'd6; // SLL
                        Shift_count = rs;
                        W_en_mem = 1'b0;
                        Sel_Din = 1'b0;
                        I_O = 1'b0;
                    end
                    4'd1: begin // SLR
                        W_en_reg = 1'b1;
                        Sel_AC = 1'b1;
                        W_addr = rd;
                        R_addr_A = rd;
                        R_addr_B = 4'd0;
                        Address_Sel = PC;
                        Control_PC = 2'b10;
                        operation = 4'd7; // SLR
                        Shift_count = rs;
                        W_en_mem = 1'b0;
                        Sel_Din = 1'b0;
                        I_O = 1'b0;
                    end
                    4'd2: begin // SAR
                        W_en_reg = 1'b1;
                        Sel_AC = 1'b1;
                        W_addr = rd;
                        R_addr_A = rd;
                        R_addr_B = 4'd0;
                        Address_Sel = PC;
                        Control_PC = 2'b10;
                        operation = 4'd8; // SAR
                        Shift_count = rs;
                        W_en_mem = 1'b0;
                        Sel_Din = 1'b0;
                        I_O = 1'b0;
                    end
                    default: begin
                        // NOP
                        W_en_reg = 1'b0;
                        Sel_AC = 1'b0;
                        W_addr = 4'b0;
                        R_addr_A = 4'b0;
                        R_addr_B = 4'b0;
                        Address_Sel = PC;
                        Control_PC = 2'b10;
                        operation = 4'b0;
                        Shift_count = 4'b0;
                        W_en_mem = 1'b0;
                        Sel_Din = 1'b0;
                        I_O = 1'b0;
                    end
                endcase
            end
            4'd8: begin // MOVE
                W_en_reg = 1'b1;
                Sel_AC = 1'b0;
                W_addr = rd;
                R_addr_A = rs;
                R_addr_B = 4'b0;
                Address_Sel = PC;
                Control_PC = 2'b10;
                operation = 4'b0;
                Shift_count = 4'b0;
                W_en_mem = 1'b0;
                Sel_Din = 1'b0;
                I_O = 1'b0;
            end
            4'd9: begin // LOAD
                W_en_reg = 1'b1;
                Sel_AC = 1'b1;
                W_addr = rd;
                R_addr_A = 4'b0;
                R_addr_B = 4'b0;
                Address_Sel = rs;
                Control_PC = 2'b00;
                operation = 4'b0;
                Shift_count = 4'b0;
                W_en_mem = 1'b0;
                Sel_Din = 1'b1;
                I_O = 1'b0;
            end
            4'd10: begin // STORE
                W_en_reg = 1'b0;
                Sel_AC = 1'b0;
                W_addr = 4'd0;
                R_addr_A = rd;
                R_addr_B = 4'b0;
                Address_Sel = rs;
                Control_PC = 2'b00;
                operation = 4'b0;
                Shift_count = 4'b0;
                W_en_mem = 1'b1;
                Sel_Din = 1'b0;
                I_O = 1'b0;
            end
            4'd11: begin // LOAD immediate
                W_en_reg = 1'b1;
                Sel_AC = 1'b1;
                W_addr = rd;
                R_addr_A = 4'b0;
                R_addr_B = 4'b0;
                Address_Sel = PC;
                Control_PC = 2'b10;
                operation = 4'b0;
                Shift_count = 4'b0;
                W_en_mem = 1'b0;
                Sel_Din = 1'b1;
                I_O = 1'b0;
            end
            4'd12: begin // CALL
                W_en_reg = 1'b1;
                Sel_AC = 1'b0;
                W_addr = rd;
                R_addr_A = PC;
                R_addr_B = rs;
                Address_Sel = PC;
                Control_PC = 2'b01;
                operation = 4'd10;
                Shift_count = 4'b0;
                W_en_mem = 1'b0;
                Sel_Din = 1'b0;
                I_O = 1'b0;
            end
            4'd13: begin // BRANCH
                case (func)
                    4'd0: begin // if Equal
                        if (cmp_in[1]) begin
                            W_en_reg = 1'b1;
                            Sel_AC = 1'b1;
                            W_addr = PC;
                            R_addr_A = rd;
                            R_addr_B = rs;
                            Address_Sel = PC;
                            Control_PC = 2'b00;
                            operation = 4'b0;
                            Shift_count = 4'b0;
                            W_en_mem = 1'b0;
                            Sel_Din = 1'b1;
                            I_O = 1'b0;
                        end else begin
                            W_en_reg = 1'b0;
                            Sel_AC = 1'b0;
                            W_addr = 4'b0;
                            R_addr_A = rd;
                            R_addr_B = rs;
                            Address_Sel = PC;
                            Control_PC = 2'b10;
                            operation = 4'b0;
                            Shift_count = 4'b0;
                            W_en_mem = 1'b0;
                            Sel_Din = 1'b0;
                            I_O = 1'b0;
                        end
                    end
                    4'd1: begin // if not Equal
                        if (~cmp_in[1]) begin
                            W_en_reg = 1'b1;
                            Sel_AC = 1'b1;
                            W_addr = PC;
                            R_addr_A = rd;
                            R_addr_B = rs;
                            Address_Sel = PC;
                            Control_PC = 2'b00;
                            operation = 4'b0;
                            Shift_count = 4'b0;
                            W_en_mem = 1'b0;
                            Sel_Din = 1'b1;
                            I_O = 1'b0;
                        end else begin
                            W_en_reg = 1'b0;
                            Sel_AC = 1'b0;
                            W_addr = 4'b0;
                            R_addr_A = rd;
                            R_addr_B = rs;
                            Address_Sel = PC;
                            Control_PC = 2'b10;
                            operation = 4'b0;
                            Shift_count = 4'b0;
                            W_en_mem = 1'b0;
                            Sel_Din = 1'b0;
                            I_O = 1'b0;
                        end
                    end
                    4'd2: begin // if less than
                        if (cmp_in[0]) begin
                            W_en_reg = 1'b1;
                            Sel_AC = 1'b1;
                            W_addr = PC;
                            R_addr_A = rd;
                            R_addr_B = rs;
                            Address_Sel = PC;
                            Control_PC = 2'b00;
                            operation = 4'b0;
                            Shift_count = 4'b0;
                            W_en_mem = 1'b0;
                            Sel_Din = 1'b1;
                            I_O = 1'b0;
                        end else begin
                            W_en_reg = 1'b0;
                            Sel_AC = 1'b0;
                            W_addr = 4'b0;
                            R_addr_A = rd;
                            R_addr_B = rs;
                            Address_Sel = PC;
                            Control_PC = 2'b10;
                            operation = 4'b0;
                            Shift_count = 4'b0;
                            W_en_mem = 1'b0;
                            Sel_Din = 1'b0;
                            I_O = 1'b0;
                        end
                    end
                    4'd3: begin // if greater than
                        if (cmp_in[2]) begin
                            W_en_reg = 1'b1;
                            Sel_AC = 1'b1;
                            W_addr = PC;
                            R_addr_A = rd;
                            R_addr_B = rs;
                            Address_Sel = PC;
                            Control_PC = 2'b00;
                            operation = 4'b0;
                            Shift_count = 4'b0;
                            W_en_mem = 1'b0;
                            Sel_Din = 1'b1;
                            I_O = 1'b0;
                        end else begin
                            W_en_reg = 1'b0;
                            Sel_AC = 1'b0;
                            W_addr = 4'b0;
                            R_addr_A = rd;
                            R_addr_B = rs;
                            Address_Sel = PC;
                            Control_PC = 2'b10;
                            operation = 4'b0;
                            Shift_count = 4'b0;
                            W_en_mem = 1'b0;
                            Sel_Din = 1'b0;
                            I_O = 1'b0;
                        end
                    end
                    4'd4: begin // if less than or equal
                        if (cmp_in[0] | cmp_in[1]) begin
                            W_en_reg = 1'b1;
                            Sel_AC = 1'b1;
                            W_addr = PC;
                            R_addr_A = rd;
                            R_addr_B = rs;
                            Address_Sel = PC;
                            Control_PC = 2'b00;
                            operation = 4'b0;
                            Shift_count = 4'b0;
                            W_en_mem = 1'b0;
                            Sel_Din = 1'b1;
                            I_O = 1'b0;
                        end else begin
                            W_en_reg = 1'b0;
                            Sel_AC = 1'b0;
                            W_addr = 4'b0;
                            R_addr_A = rd;
                            R_addr_B = rs;
                            Address_Sel = PC;
                            Control_PC = 2'b10;
                            operation = 4'b0;
                            Shift_count = 4'b0;
                            W_en_mem = 1'b0;
                            Sel_Din = 1'b0;
                            I_O = 1'b0;
                        end
                    end
                    4'd5: begin // if greater than or equal
                        if (cmp_in[1] | cmp_in[2]) begin
                            W_en_reg = 1'b1;
                            Sel_AC = 1'b1;
                            W_addr = PC;
                            R_addr_A = rd;
                            R_addr_B = rs;
                            Address_Sel = PC;
                            Control_PC = 2'b00;
                            operation = 4'b0;
                            Shift_count = 4'b0;
                            W_en_mem = 1'b0;
                            Sel_Din = 1'b1;
                            I_O = 1'b0;
                        end else begin
                            W_en_reg = 1'b0;
                            Sel_AC = 1'b0;
                            W_addr = 4'b0;
                            R_addr_A = rd;
                            R_addr_B = rs;
                            Address_Sel = PC;
                            Control_PC = 2'b10;
                            operation = 4'b0;
                            Shift_count = 4'b0;
                            W_en_mem = 1'b0;
                            Sel_Din = 1'b0;
                            I_O = 1'b0;
                        end
                    end
                    default: begin // NOP
                        W_en_reg = 1'b0;
                        Sel_AC = 1'b0;
                        W_addr = 4'b0;
                        R_addr_A = rd;
                        R_addr_B = rs;
                        Address_Sel = PC;
                        Control_PC = 2'b10;
                        operation = 4'b0;
                        Shift_count = 4'b0;
                        W_en_mem = 1'b0;
                        Sel_Din = 1'b0;
                        I_O = 1'b0;
                    end
                endcase
            end
            4'd14: begin // IN
                W_en_reg = 1'b1;
                Sel_AC = 1'b1;
                W_addr = rd;
                R_addr_A = 4'b0;
                R_addr_B = 4'b0;
                Address_Sel = rs;
                Control_PC = 2'b00;
                operation = 4'b0;
                Shift_count = 4'b0;
                W_en_mem = 1'b0;
                Sel_Din = 1'b1;
                I_O = 1'b1;
            end
            4'd15: begin // OUT
                W_en_reg = 1'b0;
                Sel_AC = 1'b0;
                W_addr = 4'd0;
                R_addr_A = rd;
                R_addr_B = 4'b0;
                Address_Sel = rs;
                Control_PC = 2'b00;
                operation = 4'b0;
                Shift_count = 4'b0;
                W_en_mem = 1'b1;
                Sel_Din = 1'b0;
                I_O = 1'b1;
            end
            default : begin
                // NOP
                W_en_reg = 1'b0;
                Sel_AC = 1'b0;
                W_addr = 4'b0;
                R_addr_A = 4'b0;
                R_addr_B = 4'b0;
                Address_Sel = PC;
                Control_PC = 2'b10;
                operation = 4'b0;
                Shift_count = 4'b0;
                W_en_mem = 1'b0;
                Sel_Din = 1'b0;
                I_O = 1'b0;
            end
        endcase
    end
endmodule