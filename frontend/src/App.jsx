import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Badge } from '@/components/ui/badge'
import { Search, BookOpen } from 'lucide-react'
import './App.css'

function App() {
  const [questoes, setQuestoes] = useState([])
  const [questoesFiltradas, setQuestoesFiltradas] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedAlternatives, setSelectedAlternatives] = useState({})
  const [showExplanation, setShowExplanation] = useState({})
  
  // Estados dos filtros
  const [filtros, setFiltros] = useState({
    busca: '',
    materia: '',
    assunto: '',
    ano: '',
    vestibular: ''
  })
  
  // Opções disponíveis para filtros
  const [opcoesFiltros, setOpcoesFiltros] = useState({
    materias: [],
    assuntos: [],
    anos: [],
    vestibulares: []
  })

  useEffect(() => {
    fetchQuestoes()
  }, [])

  useEffect(() => {
    aplicarFiltros()
  }, [questoes, filtros])

  const fetchQuestoes = async () => {
    try {
      const response = await fetch('/api/questoes_pas_uem') 
      const data = await response.json()
      setQuestoes(data || [])
      
      // Extrair opções únicas para os filtros
      if (data && data.length > 0) {
        const materias = [...new Set(data.map(q => q.materia))].sort()
        const assuntos = [...new Set(data.map(q => q.assunto))].sort()
        const anos = [...new Set(data.map(q => q.ano))].sort((a, b) => b - a)
        const vestibulares = [...new Set(data.map(q => q.vestibular))].sort()
        
        setOpcoesFiltros({
          materias,
          assuntos,
          anos,
          vestibulares
        })
      }
    } catch (error) {
      console.error('Erro ao carregar questões:', error)
    } finally {
      setLoading(false)
    }
  }

  const aplicarFiltros = () => {
    let questoesFiltradas = [...questoes]

    // Filtro por busca de texto
    if (filtros.busca) {
      questoesFiltradas = questoesFiltradas.filter(questao =>
        questao.enunciado.toLowerCase().includes(filtros.busca.toLowerCase()) ||
        questao.assunto.toLowerCase().includes(filtros.busca.toLowerCase())
      )
    }

    // Filtro por matéria
    if (filtros.materia) {
      questoesFiltradas = questoesFiltradas.filter(questao =>
        questao.materia === filtros.materia
      )
    }

    // Filtro por assunto
    if (filtros.assunto) {
      questoesFiltradas = questoesFiltradas.filter(questao =>
        questao.assunto === filtros.assunto
      )
    }

    // Filtro por ano
    if (filtros.ano) {
      questoesFiltradas = questoesFiltradas.filter(questao =>
        questao.ano.toString() === filtros.ano
      )
    }

    // Filtro por vestibular
    if (filtros.vestibular) {
      questoesFiltradas = questoesFiltradas.filter(questao =>
        questao.vestibular === filtros.vestibular
      )
    }

    setQuestoesFiltradas(questoesFiltradas)
  }

  const handleFiltroChange = (campo, valor) => {
    setFiltros(prev => ({
      ...prev,
      [campo]: valor
    }))
  }

  const limparFiltros = () => {
    setFiltros({
      busca: '',
      materia: '',
      assunto: '',
      ano: '',
      vestibular: ''
    })
  }

  const handleAlternativeClick = (questaoId, altNumeracao) => {
    setSelectedAlternatives(prev => {
      const currentSelected = prev[questaoId] || []
      if (currentSelected.includes(altNumeracao)) {
        return { ...prev, [questaoId]: currentSelected.filter(n => n !== altNumeracao) }
      } else {
        return { ...prev, [questaoId]: [...currentSelected, altNumeracao].sort() }
      }
    })
  }

  const checkAnswer = (questaoId, correctAlternatives) => {
    const userSelection = selectedAlternatives[questaoId] || []
    const correctSum = correctAlternatives.reduce((sum, num) => sum + parseInt(num), 0)
    const userSum = userSelection.reduce((sum, num) => sum + parseInt(num), 0)
    
    return correctSum === userSum
  }

  const handleShowExplanation = (questaoId) => {
    setShowExplanation(prev => ({ ...prev, [questaoId]: !prev[questaoId] }))
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center space-x-2">
            <BookOpen className="h-8 w-8 text-blue-600" />
            <h1 className="text-2xl font-bold text-gray-900">Banco de Questões</h1>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="container mx-auto px-4 py-8">
        <div className="space-y-6">
          <h2 className="text-3xl font-bold text-gray-900">Questões</h2>
          
          {/* Filtros */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Search className="h-5 w-5" />
                <span>Filtros de Busca</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {/* Busca por texto */}
                <div className="space-y-2">
                  <label className="text-sm font-medium">Buscar no enunciado</label>
                  <Input
                    placeholder="Digite palavras-chave..."
                    value={filtros.busca}
                    onChange={(e) => handleFiltroChange('busca', e.target.value)}
                  />
                </div>

                {/* Filtro por matéria */}
                <div className="space-y-2">
                  <label className="text-sm font-medium">Matéria</label>
                  <Select value={filtros.materia} onValueChange={(value) => handleFiltroChange('materia', value)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Todas as matérias" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all-materias">Todas as matérias</SelectItem>
                      {opcoesFiltros.materias.map(materia => (
                        <SelectItem key={materia} value={materia}>{materia}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {/* Filtro por assunto */}
                <div className="space-y-2">
                  <label className="text-sm font-medium">Assunto</label>
                  <Select value={filtros.assunto} onValueChange={(value) => handleFiltroChange('assunto', value)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Todos os assuntos" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all-assuntos">Todos os assuntos</SelectItem>
                      {opcoesFiltros.assuntos.map(assunto => (
                        <SelectItem key={assunto} value={assunto}>{assunto}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {/* Filtro por ano */}
                <div className="space-y-2">
                  <label className="text-sm font-medium">Ano</label>
                  <Select value={filtros.ano} onValueChange={(value) => handleFiltroChange('ano', value)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Todos os anos" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all-anos">Todos os anos</SelectItem>
                      {opcoesFiltros.anos.map(ano => (
                        <SelectItem key={ano} value={ano.toString()}>{ano}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {/* Filtro por vestibular */}
                <div className="space-y-2">
                  <label className="text-sm font-medium">Vestibular</label>
                  <Select value={filtros.vestibular} onValueChange={(value) => handleFiltroChange('vestibular', value)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Todos os vestibulares" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all-vestibulares">Todos os vestibulares</SelectItem>
                      {opcoesFiltros.vestibulares.map(vestibular => (
                        <SelectItem key={vestibular} value={vestibular}>{vestibular}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {/* Botão limpar filtros */}
                <div className="space-y-2">
                  <label className="text-sm font-medium">&nbsp;</label>
                  <Button 
                    variant="outline" 
                    onClick={limparFiltros}
                    className="w-full"
                  >
                    Limpar Filtros
                  </Button>
                </div>
              </div>
              
              {/* Contador de resultados */}
              <div className="mt-4 text-sm text-gray-600">
                {loading ? 'Carregando...' : `${questoesFiltradas.length} questão(ões) encontrada(s)`}
              </div>
            </CardContent>
          </Card>

          {loading ? (
            <div className="text-center py-8">
              <p>Carregando questões...</p>
            </div>
          ) : questoesFiltradas.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-gray-500">Nenhuma questão encontrada com os filtros aplicados</p>
            </div>
          ) : (
            <div className="space-y-4">
              {questoesFiltradas.map(questao => (
                <Card key={questao.id}>
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <Badge variant="secondary">{questao.vestibular} {questao.ano}</Badge>
                        <Badge variant="outline">{questao.materia}</Badge>
                        <Badge variant="outline">{questao.assunto}</Badge>
                      </div>
                      <span className="text-sm text-gray-500">Questão {questao.numero}</span>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className="whitespace-pre-wrap mb-4">{questao.enunciado}</p>
                    <div className="space-y-2">
                      {questao.alternativas.map((alt, index) => {
                        const altNumeration = questao.alternativas_numeracao[index]
                        const isSelected = (selectedAlternatives[questao.id] || []).includes(altNumeration)
                        const isCorrect = (questao.alternativas_corretas || []).includes(altNumeration)
                        const isAnswerChecked = showExplanation[questao.id]

                        let bgColor = 'bg-gray-100 hover:bg-gray-200'
                        if (isAnswerChecked) {
                          if (isCorrect) {
                            bgColor = 'bg-green-100'
                          } else if (isSelected && !isCorrect) {
                            bgColor = 'bg-red-100'
                          }
                        } else if (isSelected) {
                          bgColor = 'bg-blue-100'
                        }

                        return (
                          <div
                            key={altNumeration}
                            className={`p-3 rounded-md cursor-pointer flex items-start space-x-3 ${bgColor}`}
                            onClick={() => handleAlternativeClick(questao.id, altNumeration)}
                          >
                            <span className="font-bold text-gray-700">{altNumeration})</span>
                            <p className="flex-1">{alt}</p>
                          </div>
                        )
                      })}
                    </div>
                    <div className="mt-4 flex justify-between items-center">
                      <Button 
                        onClick={() => handleShowExplanation(questao.id)}
                        variant="outline"
                      >
                        {showExplanation[questao.id] ? 'Esconder Explicação' : 'Verificar Resposta e Explicação'}
                      </Button>
                      {showExplanation[questao.id] && (
                        <Badge 
                          variant={checkAnswer(questao.id, questao.alternativas_corretas) ? 'default' : 'destructive'}
                          className="text-lg px-4 py-2"
                        >
                          Sua Resposta: {selectedAlternatives[questao.id] ? selectedAlternatives[questao.id].join(' + ') : 'Nenhuma'}
                          {checkAnswer(questao.id, questao.alternativas_corretas) ? ' (Correta)' : ' (Incorreta)'}
                        </Badge>
                      )}
                    </div>
                    {showExplanation[questao.id] && (
                      <Card className="mt-4 bg-gray-50">
                        <CardHeader>
                          <CardTitle className="text-lg">Explicação</CardTitle>
                        </CardHeader>
                        <CardContent>
                          <p className="whitespace-pre-wrap">Resposta Correta: {questao.resposta_correta}</p>
                          <p className="whitespace-pre-wrap mt-2">{questao.explicacao}</p>
                        </CardContent>
                      </Card>
                    )}
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  )
}

export default App

