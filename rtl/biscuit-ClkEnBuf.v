
`ifndef BISCUIT_CLKENBUF_V
`define BISCUIT_CLKENBUF_V

module biscuit_ClkEnBuf (clk, rclk, en_l);
output clk;
input  rclk, en_l;
reg    clken;

  always @ (rclk or en_l)
    if (!rclk)
      clken = !en_l ;
  assign clk = clken & rclk;

endmodule

`endif