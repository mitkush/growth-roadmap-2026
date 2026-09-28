# Seeds realistic volumes quickly with SQL generate_series (not one INSERT per row).
#
#   bin/rails db:seed                 # full size (about 2.8M rows, a few minutes)
#   SEED_SCALE=0.1 bin/rails db:seed  # 10% for a quick start
#
# Deliberately NOT indexed: orders.status, orders.placed_at, events.occurred_at.
# Finding and fixing that is part of Step 2.
scale = Float(ENV.fetch("SEED_SCALE", "1"))
counts = {
  customers: 20_000, products: 20_000, orders: 200_000, line_items: 600_000, events: 2_000_000
}.transform_values { |n| [(n * scale).to_i, 1].max }

conn = ActiveRecord::Base.connection
started = Process.clock_gettime(Process::CLOCK_MONOTONIC)
puts "Seeding #{counts.inspect}"

conn.execute("TRUNCATE line_items, orders, products, customers, events RESTART IDENTITY CASCADE")

conn.execute(<<~SQL)
  INSERT INTO customers (name, email, created_at, updated_at)
  SELECT 'Customer ' || g, 'customer' || g || '@example.com', now(), now()
  FROM generate_series(1, #{counts[:customers]}) AS g
SQL

conn.execute(<<~SQL)
  INSERT INTO products (name, sku, price_cents, category, created_at, updated_at)
  SELECT 'Product ' || g, 'SKU-' || lpad(g::text, 6, '0'), 100 + (random() * 9900)::int,
         (ARRAY['books', 'games', 'garden', 'kitchen', 'office', 'toys'])[1 + (g % 6)], now(), now()
  FROM generate_series(1, #{counts[:products]}) AS g
SQL

conn.execute(<<~SQL)
  INSERT INTO orders (customer_id, status, total_cents, placed_at, created_at, updated_at)
  SELECT 1 + (random() * (#{counts[:customers]} - 1))::int,
         (ARRAY['pending', 'paid', 'paid', 'paid', 'shipped', 'refunded'])[1 + (g % 6)],
         0, now() - random() * interval '365 days', now(), now()
  FROM generate_series(1, #{counts[:orders]}) AS g
SQL

conn.execute(<<~SQL)
  INSERT INTO line_items (order_id, product_id, quantity, unit_price_cents, created_at, updated_at)
  SELECT 1 + (random() * (#{counts[:orders]} - 1))::int, 1 + (random() * (#{counts[:products]} - 1))::int,
         1 + (random() * 4)::int, 100 + (random() * 9900)::int, now(), now()
  FROM generate_series(1, #{counts[:line_items]}) AS g
SQL

conn.execute(<<~SQL)
  UPDATE orders SET total_cents = t.total
  FROM (SELECT order_id, SUM(quantity * unit_price_cents) AS total FROM line_items GROUP BY order_id) AS t
  WHERE orders.id = t.order_id
SQL

conn.execute(<<~SQL)
  INSERT INTO events (name, payload, occurred_at, created_at, updated_at)
  SELECT (ARRAY['page_view', 'add_to_cart', 'checkout', 'search'])[1 + (g % 4)],
         jsonb_build_object('customer_id', 1 + (random() * (#{counts[:customers]} - 1))::int),
         now() - random() * interval '365 days', now(), now()
  FROM generate_series(1, #{counts[:events]}) AS g
SQL

conn.execute("ANALYZE")
elapsed = Process.clock_gettime(Process::CLOCK_MONOTONIC) - started
puts format("Done in %.1fs: %s", elapsed, counts.keys.map { |t| "#{t}=#{conn.select_value("SELECT count(*) FROM #{t}")}" }.join(", "))
