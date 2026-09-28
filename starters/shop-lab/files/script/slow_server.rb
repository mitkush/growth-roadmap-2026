# A tiny HTTP server that answers every request after DELAY_MS (default 100 ms).
# It stands in for a slow external API. Run it in its own terminal:
#
#   ruby script/slow_server.rb          # listens on 127.0.0.1:4567
require "socket"

delay = Integer(ENV.fetch("DELAY_MS", "100")) / 1000.0
server = TCPServer.new("127.0.0.1", Integer(ENV.fetch("PORT", "4567")))
puts "slow server listening on 127.0.0.1:#{server.addr[1]} (delay #{(delay * 1000).round} ms)"

loop do
  Thread.new(server.accept) do |client|
    client.gets                                            # request line
    while (line = client.gets) && line != "\r\n"; end      # skip headers
    sleep delay
    body = "ok"
    client.write "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n" \
                 "Content-Length: #{body.bytesize}\r\nConnection: close\r\n\r\n#{body}"
    client.close
  end
end
