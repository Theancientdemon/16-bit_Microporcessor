/*
    Testbench for a 16-bit Processor
        -> Initialize Processor, RAM and IO devices.
        -> Provides interconnections
        -> Simulation and Verification
*/

`timescale 1ps/1ps

module Processor16_tb;

    // Testbench signals
    localparam CLK_PERIOD = 10;
    reg CLK;                    // Clock Signal
    reg RST;                    // Reset Signal

    wire [15:0] Data_in;        // Data input from memory
    wire [15:0] Data_out;       // Data output to memory
    wire [15:0] Address_bus;    // Address output to memory

    wire Write, Read, IO;       // Control signals for memory

    // Initialization
    // Processor
    Processor16 Dut (
        .CLK_in(CLK),
        .RST(RST),
        .Data_in(Data_in),          // Data input to Processor from memory
        .Data_out(Data_out),        // Data output to memory
        .Address_out(Address_bus),  // Address output to memory
        .W_en(Write),               // Write enable signal for memory
        .R_en(Read),                // Read enable signal for memory
        .I_O(IO)                    // IO signal
    );

    // RAM
    RAM memory (
        .CLK(CLK),
        .Data_in(Data_out),
        .Data_out(Data_in),
        .Address_bus(Address_bus),
        .Write(Write && !IO),       // Write if write signal is present but IO signal is NOT
        .Read(Read)
    );

    // IO device(display)
    Display display (
        .CLK(CLK),
        .Data_in(Data_out),
        .enable(Write && IO)        // Write if write and IO signals are both high
    );

    // Initial Reset Block
    initial begin
        CLK = 0;
        RST = 1;
        #CLK_PERIOD RST = 0;
    end

    // Clock generation
    always #(CLK_PERIOD/2) CLK = ~CLK;

    // VCD dump generation
    initial begin
        $dumpfile("Processor16_tb.vcd");
        $dumpvars(0, Processor16_tb);
    end

    // Simulation ends when Processor is Halted
    always @(Dut.Halted) begin
        if (Dut.Halted) begin
            #10 $finish;
        end
    end

endmodule
