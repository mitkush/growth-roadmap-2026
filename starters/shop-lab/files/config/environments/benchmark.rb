# Production-like settings for local benchmarks (Steps 1-2): eager loading, no code reloading,
# caching on, quiet logs, but plain HTTP, one database (development) and no Solid Queue/Cache setup.
#
#   RAILS_ENV=benchmark bin/rails server
require "active_support/core_ext/integer/time"

Rails.application.configure do
  config.enable_reloading = false
  config.eager_load = true
  config.consider_all_requests_local = false
  config.action_controller.perform_caching = true
  config.cache_store = :memory_store
  config.active_job.queue_adapter = :async
  config.log_level = :warn
  config.logger = ActiveSupport::TaggedLogging.logger($stdout)
  config.active_support.report_deprecations = false
  config.active_record.dump_schema_after_migration = false
  config.yjit = ENV.fetch("YJIT", "1") != "0"  # YJIT=0 bin/rails server to compare without YJIT
end
