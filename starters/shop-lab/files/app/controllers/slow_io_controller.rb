require "net/http"

# Waits on a slow upstream service (script/slow_server.rb): pure I/O, so it releases the GVL.
class SlowIoController < ApplicationController
  SLOW_URL = URI(ENV.fetch("SLOW_SERVICE_URL", "http://127.0.0.1:4567/"))

  def show
    render json: { upstream: Net::HTTP.get(SLOW_URL) }
  end
end
