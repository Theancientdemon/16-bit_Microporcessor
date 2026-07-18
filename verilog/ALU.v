/*
    Arithmetic and Logical Unit.
        -> Performs Arithmetic Operations.
        -> Performs Logical Operations.
        -> Performs Shifting Operations.
        -> Can pass Values of Data Buses as it is.
        -> Uses operation signal from CU to decide operation.
        -> only one operation at a time.
        -> Outputs comparision of boths inputs as cmp_out
*/

`timescale 1ps/1ps

module ALU (
    input  wire [3:0] operation,        // Operation Select
    input  wire [3:0] Shift_count,      // Count for shift operation

    input  wire [15:0] A_bus,           // Input Bus A
    input wire [15:0] B_bus,            // Input Bus B

    output reg [15:0] C_bus,            // Output Bus C
    output reg [2:0] cmp_out            // Comparator output
);

    // Defining operations
    localparam  ADD = 4'd0,
                SUB = 4'd1,
                AND = 4'd2,
                OR  = 4'd3,
                XOR = 4'd4,
                NOT = 4'd5,
                SLL = 4'd6,
                SLR = 4'd7,
                SAR = 4'd8,
                Pass_A = 4'd9,
                Pass_B = 4'd10;

    always @(*) begin
        case (operation)
            ADD: begin
                C_bus = A_bus + B_bus;
            end
            SUB: begin
                C_bus = A_bus - B_bus;
            end
            AND: begin
                C_bus = A_bus & B_bus;
            end
            OR: begin
                C_bus = A_bus | B_bus;
            end
            XOR: begin
                C_bus = A_bus ^ B_bus;
            end
            NOT: begin
                C_bus = ~A_bus;
            end
            SLL: begin
                C_bus = A_bus << Shift_count; // Shift left logical
            end
            SLR: begin
                C_bus = A_bus >> Shift_count; // Shift right logical
            end
            SAR: begin
                C_bus = A_bus >>> Shift_count; // Shift right arithmetic
            end
            Pass_A: begin
                C_bus = A_bus;
            end
            Pass_B: begin
                C_bus = B_bus;
            end
            default: begin
                C_bus = A_bus;
            end
        endcase
    end

    // Comparator
    always @(*) begin
        cmp_out = {A_bus < B_bus, A_bus == B_bus, A_bus > B_bus};
    end

endmodule