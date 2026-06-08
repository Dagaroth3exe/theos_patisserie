import styles from "./page.module.css";

const featuredProducts = [
  {
    name: "Rose Pistachio Éclair",
    description: "Silky rose crème, pistachio praline, and hand-tempered glaze.",
    price: "₹740",
  },
  {
    name: "Madagascar Chocolate Entremet",
    description: "70% dark chocolate mousse layered with hazelnut croustillant.",
    price: "₹1,280",
  },
  {
    name: "Saffron Citrus Tart",
    description: "Saffron custard, candied citrus, and almond sable crust.",
    price: "₹860",
  },
];

export default function Home() {
  return (
    <div className={styles.page}>
      <header className={styles.hero}>
        <p className={styles.kicker}>Theo&apos;s Patisserie • India</p>
        <h1>Luxury desserts crafted for celebrations that deserve elegance.</h1>
        <p className={styles.lead}>
          Discover a refined collection of handcrafted pastries, plated cakes,
          and tasting boxes prepared in small batches by our pastry atelier.
        </p>
        <a className={styles.primaryCta} href="#order">
          Order Online
        </a>
      </header>

      <main className={styles.main}>
        <section className={styles.section}>
          <h2>Featured Product Showcase</h2>
          <div className={styles.grid}>
            {featuredProducts.map((item) => (
              <article className={styles.card} key={item.name}>
                <h3>{item.name}</h3>
                <p>{item.description}</p>
                <span>{item.price}</span>
              </article>
            ))}
          </div>
        </section>

        <section className={styles.section} id="order">
          <h2>Online Ordering</h2>
          <p>
            Place pre-orders for curated dessert boxes, signature cakes, and
            gifting hampers with same-day concierge support across major Indian
            metros.
          </p>
          <a className={styles.secondaryCta} href="mailto:orders@theospatisserie.in">
            Start Your Order
          </a>
        </section>

        <section className={styles.section}>
          <h2>Brand Story</h2>
          <p>
            Theo&apos;s Patisserie blends classical French technique with Indian
            ingredients sourced from trusted farms. Every collection is designed
            to celebrate artful indulgence, from intimate dinners to grand
            festive occasions.
          </p>
        </section>
      </main>
    </div>
  );
}
