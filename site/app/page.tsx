'use client';

import { useMemo, useState } from 'react';
import { Code2, ExternalLink, FileCheck2, Search, ShieldCheck } from 'lucide-react';
import manifest from '../data/benchmark-manifest.json';

const repository = 'https://github.com/linhaquenaoquebra-sudo/toolcommons';
const capabilities = new Map(manifest.capabilities.map((item) => [item.id, item]));
const tasks = new Map(manifest.tasks.map((item) => [item.id, item]));

export default function Home() {
  const [query, setQuery] = useState('');
  const [status, setStatus] = useState<'all' | 'passed' | 'failed'>('all');
  const results = useMemo(() => {
    const needle = query.trim().toLowerCase();
    return manifest.results.filter((result) => {
      const tool = capabilities.get(result.capabilityId);
      const task = tasks.get(result.taskId);
      const text = [tool?.name, result.toolVersion, task?.title, result.pipelineId, result.status,
        result.environment.os, result.environment.python].join(' ').toLowerCase();
      return (status === 'all' || result.status === status) && (!needle || text.includes(needle));
    });
  }, [query, status]);
  const passing = manifest.results.filter((result) => result.status === 'passed').length;

  return (
    <main className="min-h-screen bg-[#f7f4ed] text-[#102b3a]">
      <header className="border-b border-[#102b3a]/10 bg-[#f7f4ed]/95">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-5 py-5 sm:px-8">
          <a href="#top" className="flex items-center gap-3 font-semibold tracking-tight">
            <span className="grid size-9 place-items-center rounded-xl bg-[#0a756c] text-white">TC</span>
            <span>ToolCommons</span>
          </a>
          <a className="flex items-center gap-2 text-sm font-medium hover:text-[#0a756c]" href={repository} target="_blank" rel="noreferrer"><Code2 className="size-4" /> Código aberto</a>
        </div>
      </header>

      <section id="top" className="mx-auto max-w-7xl px-5 pb-12 pt-14 sm:px-8 sm:pt-20">
        <div className="grid gap-10 lg:grid-cols-[1.35fr_.65fr] lg:items-end">
          <div>
            <p className="mb-4 text-xs font-bold uppercase tracking-[.2em] text-[#0a756c]">Evidence before preference</p>
            <h1 className="max-w-4xl text-4xl font-semibold leading-[1.05] tracking-[-.04em] sm:text-6xl">Escolher ferramentas com provas reproduzíveis.</h1>
            <p className="mt-6 max-w-2xl text-lg leading-8 text-[#43606d]">Um manifesto pesquisável de testes públicos. Cada resultado liga à respetiva receita, ambiente e métricas — para humanos e agentes.</p>
          </div>
          <aside className="rounded-3xl border border-[#0a756c]/20 bg-[#dcebe5] p-6">
            <ShieldCheck className="mb-4 size-7 text-[#0a756c]" />
            <p className="font-semibold">Não é um ranking universal.</p>
            <p className="mt-2 text-sm leading-6 text-[#43606d]">É evidência delimitada por tarefa, versão, pipeline e ambiente. O contexto permanece visível.</p>
          </aside>
        </div>
        <dl className="mt-12 grid grid-cols-2 gap-px overflow-hidden rounded-2xl border border-[#102b3a]/10 bg-[#102b3a]/10 sm:grid-cols-4">
          {([['Ferramentas', manifest.capabilities.length], ['Benchmarks', manifest.tasks.length], ['Execuções', manifest.results.length], ['Aprovadas', passing]] as const).map(([label, value]) => (
            <div className="bg-[#fffdf8] p-5" key={label}><dt className="text-xs font-bold uppercase tracking-wider text-[#6a7f88]">{label}</dt><dd className="mt-2 text-3xl font-semibold">{value}</dd></div>
          ))}
        </dl>
      </section>

      <section className="mx-auto max-w-7xl px-5 pb-20 sm:px-8">
        <div className="rounded-3xl border border-[#102b3a]/10 bg-[#fffdf8] shadow-[0_18px_50px_rgba(16,43,58,.06)]">
          <div className="border-b border-[#102b3a]/10 p-5 sm:p-7">
            <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
              <div><h2 className="text-2xl font-semibold tracking-tight">Manifesto de benchmarks</h2><p className="mt-1 text-sm text-[#617680]">Pesquisa por ferramenta, tarefa, pipeline, estado, sistema ou versão.</p></div>
              <div className="flex flex-col gap-3 sm:flex-row">
                <label className="relative block"><Search className="absolute left-3 top-1/2 size-4 -translate-y-1/2 text-[#6a7f88]" /><span className="sr-only">Pesquisar resultados</span><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Pesquisar…" className="h-11 w-full rounded-xl border border-[#102b3a]/15 bg-white pl-10 pr-4 outline-none focus:border-[#0a756c] sm:w-72" /></label>
                <div className="flex rounded-xl bg-[#edf1ee] p-1" aria-label="Filtrar por estado">
                  {(['all', 'passed', 'failed'] as const).map((item) => <button key={item} onClick={() => setStatus(item)} className={`rounded-lg px-3 py-2 text-sm font-medium ${status === item ? 'bg-white text-[#102b3a] shadow-sm' : 'text-[#617680]'}`}>{item === 'all' ? 'Todos' : item === 'passed' ? 'Aprovados' : 'Falhados'}</button>)}
                </div>
              </div>
            </div>
          </div>
          <div className="divide-y divide-[#102b3a]/10">
            {results.map((result) => {
              const tool = capabilities.get(result.capabilityId); const task = tasks.get(result.taskId);
              return <article className="grid gap-4 p-5 sm:p-7 lg:grid-cols-[1fr_1.5fr_.7fr_auto] lg:items-center" key={result.receiptPath}>
                <div><p className="font-semibold">{tool?.name}</p><p className="mt-1 text-xs text-[#6a7f88]">v{result.toolVersion} · {result.environment.python}</p></div>
                <div><p className="text-sm font-medium leading-6">{task?.title}</p><p className="mt-1 font-mono text-xs text-[#6a7f88]">{result.pipelineId}</p></div>
                <div className="flex items-center gap-3 lg:block"><span className={`inline-flex rounded-full px-2.5 py-1 text-xs font-bold ${result.status === 'passed' ? 'bg-[#d9eee4] text-[#116044]' : 'bg-[#f7dfda] text-[#963d31]'}`}>{result.status === 'passed' ? 'Aprovado' : 'Falhado'}</span><p className="mt-0 text-xs text-[#6a7f88] lg:mt-2">{Math.round(result.metrics.cellAccuracy * 100)}% precisão</p></div>
                <a href={`${repository}/blob/main/${result.receiptPath}`} target="_blank" rel="noreferrer" className="inline-flex h-10 items-center justify-center gap-2 rounded-xl border border-[#102b3a]/15 px-3 text-sm font-semibold hover:border-[#0a756c] hover:text-[#0a756c]">Evidência <ExternalLink className="size-3.5" /></a>
              </article>;
            })}
            {results.length === 0 && <div className="grid place-items-center px-5 py-16 text-center"><FileCheck2 className="mb-3 size-7 text-[#0a756c]" /><p className="font-semibold">Nenhum resultado corresponde à pesquisa.</p><button onClick={() => { setQuery(''); setStatus('all'); }} className="mt-2 text-sm font-semibold text-[#0a756c]">Limpar filtros</button></div>}
          </div>
        </div>
      </section>
      <footer className="border-t border-[#102b3a]/10 px-5 py-8 text-center text-sm text-[#617680]">Construído pela LQNQ — Linha que não quebra · dados e fixtures abertos</footer>
    </main>
  );
}
