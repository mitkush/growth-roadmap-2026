# A minimal load generator for when oha or wrk are not installed.
# Runs CONCURRENCY clients (threads with keep-alive connections) for SECONDS, then prints
# throughput and latency percentiles.
#
#   ruby script/load.rb http://127.0.0.1:3000/slow_io 16 15
require "net/http"

url = URI(ARGV.fetch(0) { abort "usage: ruby script/load.rb URL [concurrency=16] [seconds=15]" })
concurrency = Integer(ARGV[1] || 16)
seconds = Float(ARGV[2] || 15)

def now = Process.clock_gettime(Process::CLOCK_MONOTONIC)

latencies = Thread::Queue.new
errors = Thread::Queue.new
deadline = now + seconds

threads = Array.new(concurrency) do
  Thread.new do
    Net::HTTP.start(url.host, url.port, read_timeout: 60) do |http|
      while now < deadline
        started = now
        response = http.get(url.request_uri)
        response.is_a?(Net::HTTPSuccess) ? latencies << (now - started) : errors << response.code
      end
    end
  end
end
threads.each(&:join)

times = Array.new(latencies.size) { latencies.pop }.sort
percentile = ->(p) { (times[((times.size - 1) * p).round] * 1000).round(1) }
puts format("%s  c=%d  %ds  requests=%d  errors=%d  req/s=%.1f  p50=%sms  p95=%sms  p99=%sms",
            url.path, concurrency, seconds, times.size, errors.size, times.size / seconds,
            percentile.(0.50), percentile.(0.95), percentile.(0.99))
