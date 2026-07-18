/*
    Processor Module.
        -> Combines ALU, Control Unit and Registerfile together.
        -> Provides interconnections.
        -> Handles connections to outer modules
*/

`timescale 1ps/1ps

module Processor16(
    input wire CLK_in,                  // Clock Signal as input
    input wire RST,                     // Reset Signal.

    input wire [15:0] Data_in,          // Data input from memory
    output wire [15:0] Data_out,        // Data output to memory
    output wire [15:0] Address_out,     // Address output to memory

    output wire W_en,                   // Write enable signal for memory
    output wire R_en,                   // Read enable signal for memory
    output wire I_O                     // IO signal
);
    // Declaration of wires
    // ALU
    wire [3:0] alu_operation;
    wire [3:0] alu_shift_count;
    wire [15:0] A_bus, B_bus, C_bus, ALU_out;
    wire [2:0] cmp_out;

    // Register bank 
    wire Sel_AC;
    wire [3:0] W_addr, R_addr_A, R_addr_B, Address_Sel;
    wire [1:0] Control_PC;

    // Miscellaneous wires
    wire Halted;
    wire CLK;

    // Handle Halted state.
    // Disables Clock Signal when Halted
    assign CLK = Halted ? 1'b0 : CLK_in;

    // Selects between External input and Alu output.
    assign C_bus = Sel_Din ? Data_in : ALU_out;

    // Drives Data_out
    assign Data_out = W_en ? A_bus : 16'b0;

    // Sets Read enables as negetion of write enable.
    // Read data when not writing Data
    assign R_en = ~W_en;

    // ALU initialization
    ALU alu_inst (
        .operation(alu_operation),          // from CU(Control Unit)
        .Shift_count(alu_shift_count),      // from CU
        .A_bus(A_bus),                      // from reg bank
        .B_bus(B_bus),                      // from reg bank
        .C_bus(ALU_out),                    // to reg bank
        .cmp_out(cmp_out)                   // to CU (for branching only)
    );

    // Register Bank initialization
    Register reg_inst (
        .CLK(CLK),                          // Clock signal
        .RST(RST),                          // Reset signal
        .W_en(W_en_reg),                    // write signal
        .Sel_AC(Sel_AC),                    // Select between A and C Bus.
        .W_addr(W_addr),                    // Select Register to write.
        .R_addr_A(R_addr_A),                // Select Register to put on A Bus
        .R_addr_B(R_addr_B),                // Select Register to put on B Bus
        .Address_Sel(Address_Sel),          // Selecting a Register as Address
        .Control_PC(Control_PC),            // Program counter control
        .C_bus(C_bus),                      // C Bus 
        .A_bus(A_bus),                      // A Bus
        .B_bus(B_bus),                      // B Bus
        .Address_bus(Address_out)           // Address Bus
    );

    // Control Unit initialization
    Control_Unit CU_inst (
        .CLK(CLK),                          // Clock Signal
        .RST(RST),                          // Reset Signal
        .Fetch_input(Data_in),              // Fetch input connects to External input
        .Halted(Halted),                    // Halted state wire
        // REGISTER BANK Control signals
        .W_en_reg(W_en_reg),                // write signal to Register bank
        .Sel_AC(Sel_AC),                    // Select between A and C Bus.
        .W_addr(W_addr),                    // Select Register to write.
        .R_addr_A(R_addr_A),                // Select Register to put on A Bus
        .R_addr_B(R_addr_B),                // Select Register to put on B Bus
        .Address_Sel(Address_Sel),          // Selecting a Register as Address
        .Control_PC(Control_PC),            // Program counter control
        // ALU control signals
        .operation(alu_operation),          // Select Alu operation
        .Shift_count(alu_shift_count),      // shift operation count
        .cmp_in(cmp_out),                   // Comparator input for branching
        // Processor signals
        .W_en_mem(W_en),                    // External write signal
        .Sel_Din(Sel_Din),                  // Selects between Alu output and External input
        .I_O(I_O)                           // External IO signal
    );


endmodule