/*
    Register Bank.
        -> Has 16 16-bit register.
        -> has read-write register.
        -> R0 is read only always zero register.(Writing to it will be ignored)
*/

`timescale 1ps/1ps

module Register (
    input wire CLK,                     // Clock signal
    input wire RST,                     // Reset signal

    input  wire W_en,                   // Write enable
    input  wire Sel_AC,                 // Select A or C Bus(Sel_AC ? C_bus : A_bus)

    input  wire [3:0] W_addr,           // Write address
    input  wire [3:0] R_addr_A,         // Read address for Bus A
    input  wire [3:0] R_addr_B,         // Read address for Bus B
    input  wire [3:0] Address_Sel,      // Address selection for Address_bus

    input  wire [1:0] Control_PC,       // Control signal for Program Counter

    input  wire [15:0] C_bus,           // Data bus C

    output reg [15:0] A_bus,            // Bus A output for ALU and Memory
    output reg [15:0] B_bus,            // Bus B output for ALU
    output reg [15:0] Address_bus       // Address bus output
);

    reg [15:0] REGISTERS [15:0];        // General purpose registers
    localparam PC = 15;

    // Reset  and Write operation
    always @(posedge CLK) begin
        if (RST) begin
            for (integer i = 0; i < 16; i = i + 1) begin
                REGISTERS[i] <= 16'b0;      // Set all to zero.
            end
        end else if (W_en) begin
            if (Sel_AC) begin
                REGISTERS[W_addr] <= C_bus; // write value on C bus.
            end else begin
                REGISTERS[W_addr] <= A_bus; // write value on A bus. for move.
            end
        end
        REGISTERS[0] <= 16'b0;              // ensure, R0 is always zero.
    end

    // Control PC operations
    assign {INC_PC, Call} = Control_PC;
    always @(posedge CLK) begin
        if (INC_PC) begin
            // Auto increments Program Counter.
            REGISTERS[PC] <= REGISTERS[PC] + 1;
        end else if (Call) begin
            // Call instruction gets PC from C_bus, A_bus is used to store PC
            REGISTERS[PC] <= C_bus;
        end
    end

    // Assignment to all Buses.
    always @(*) begin
        A_bus = REGISTERS[R_addr_A];
        B_bus = REGISTERS[R_addr_B];
        Address_bus = REGISTERS[Address_Sel];
    end

endmodule