import Fastify from "fastify";
import cors from "@fastify/cors";

const app = Fastify({ logger: true });

// allow frontend calls
await app.register(cors, { origin: true });

// health check
app.get("/health", async () => ({ ok: true }));

// new POST /plan endpoint
app.post("/plan", async (req, reply) => {
  try {
    const payload = req.body;

    // forward request to MCP Python
    const res = await fetch("http://localhost:9090/plan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      throw new Error(`MCP Python error: ${res.status}`);
    }

    const data = await res.json();
    return data;
  } catch (err: any) {
    req.log.error(err);
    return reply.status(500).send({ error: String(err) });
  }
});

// start
const port = Number(process.env.PORT || 8080);
app.listen({ port, host: "0.0.0.0" }).catch((err) => {
  app.log.error(err);
  process.exit(1);
});
