/*
    Ram Module
        -> Provides 64KB of read-write memory.
        -> can use $readmemh method to load memory.
        -> can manually edit memory.
*/

`timescale 1ps/1ps

module RAM (
    input  wire CLK,                    // Clock Signal
    input wire [15:0] Data_in,          // Data input from Processor.
    output wire [15:0] Data_out,        // Data output to Processor.
    input wire [15:0] Address_bus,      // Address from Processor.
    input wire Write,                   // Write signal.
    input wire Read                     // Read signal.
);
    // Initialize 64KB of memory
    // 16-bit each (Word length)
    reg [15:0] memory [0:64*1024];

    // If Read signal is present, reads the memory at the Address given 
    // by Address_bus.
    // Asynchronous Read
    assign Data_out = memory[Address_bus];

    // Synchronous Write at posedge of Clock signal
    always @(posedge CLK) begin
        if (Write) begin
            memory[Address_bus] <= Data_in;
        end
    end

    // Using $readmemh to read a hexfile
    // initial begin
    //     $readmemh("path/to/file.txt", memory);
    // end

    // Manually Writing Bytes in the memory.
    // Comment below block if using $readmemh.
    initial begin
        memory[0] = 16'hB100;   // load r1
        memory[1] = 16'h0001;   // value
        memory[2] = 16'hB200;   // load r2
        memory[3] = 16'h000f;   // address of string
        memory[4] = 16'hB300;   // load r3
        memory[5] = 16'h0000;   // null character
        memory[6] = 16'hB500;   // load r5
        memory[7] = 16'h0008;   // address of loop
        // Label: loop
        memory[08] = 16'h9420;   // load r4 [r2]
        memory[09] = 16'hD430;   // beq r4 r3
        memory[10] = 16'h000e;   // address of end
        memory[11] = 16'hF410;   // out r4 
        memory[12] = 16'h1221;   // add r2 r2 r1
        memory[13] = 16'hC050;   // jmp to loop
        // Label: end
        memory[14] = 16'h000F;   // hlt
        // Label: string
        memory[15] = 16'h0054;
        memory[16] = 16'h0068;
        memory[17] = 16'h0069;
        memory[18] = 16'h0073;
        memory[19] = 16'h0020;
        memory[20] = 16'h0069;
        memory[21] = 16'h0073;
        memory[22] = 16'h0020;
        memory[23] = 16'h0061;
        memory[24] = 16'h0020;
        memory[25] = 16'h0031;
        memory[26] = 16'h0036;
        memory[27] = 16'h002d;
        memory[28] = 16'h0062;
        memory[29] = 16'h0069;
        memory[30] = 16'h0074;
        memory[31] = 16'h0020;
        memory[32] = 16'h0070;
        memory[33] = 16'h0072;
        memory[34] = 16'h006f;
        memory[35] = 16'h0063;
        memory[36] = 16'h0065;
        memory[37] = 16'h0073;
        memory[38] = 16'h0073;
        memory[39] = 16'h006f;
        memory[40] = 16'h0072;
        memory[41] = 16'h0020;
        memory[42] = 16'h006d;
        memory[43] = 16'h0061;
        memory[44] = 16'h0064;
        memory[45] = 16'h0065;
        memory[46] = 16'h0020;
        memory[47] = 16'h0062;
        memory[48] = 16'h0079;
        memory[49] = 16'h0020;
        memory[50] = 16'h0044;
        memory[51] = 16'h0061;
        memory[52] = 16'h0072;
        memory[53] = 16'h0073;
        memory[54] = 16'h0068;
        memory[55] = 16'h0061;
        memory[56] = 16'h006e;
        memory[57] = 16'h0020;
        memory[58] = 16'h0053;
        memory[59] = 16'h0075;
        memory[60] = 16'h0072;
        memory[61] = 16'h0079;
        memory[62] = 16'h0061;
        memory[63] = 16'h0077;
        memory[64] = 16'h0061;
        memory[65] = 16'h006e;
        memory[66] = 16'h0073;
        memory[67] = 16'h0068;
        memory[68] = 16'h0069;
        memory[69] = 16'h000a;
        memory[70] = 16'h000a;
        memory[71] = 16'h0000;
    end

endmodule

