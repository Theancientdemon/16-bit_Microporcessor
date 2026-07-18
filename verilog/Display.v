/*
    Display Module
        -> takes Data input and displays the respective number as an integer
        -> uses the $display command.
        -> displays values as ascii character.
*/

`timescale 1ps/1ps

module Display (
    input wire CLK,                 // Clock Signal
    input wire [15:0] Data_in,      // Data input to be displayed
    input wire enable               // Enable signal. Displays data when enable is high.
);
    always @(posedge CLK) begin
        if (enable) begin
            $write("%C", Data_in);
        end
    end

    // Decoration only.
    initial begin
        #1
        $display("Display:\n");
    end

endmodule