// Quick test to check Qdrant directly
import { QdrantClient } from '@qdrant/js-client-rest'

const client = new QdrantClient({
  url: 'http://localhost:6333',
})

try {
  // Check collection info
  const collectionInfo = await client.getCollection('askfiles_documents')
  console.log('📊 Collection Info:')
  console.log('  Points count:', collectionInfo.points_count)
  console.log('  Vectors count:', collectionInfo.vectors_count)
  
  // Try to scroll some points
  const scroll = await client.scroll('askfiles_documents', {
    limit: 5,
    with_payload: true,
    with_vector: false,
  })
  
  console.log('\n📝 Sample points:')
  scroll.points.forEach((point, i) => {
    console.log(`\nPoint ${i + 1}:`)
    console.log('  ID:', point.id)
    console.log('  KB ID:', point.payload?.knowledge_base_id)
    console.log('  Content:', point.payload?.content?.substring(0, 50) + '...')
  })
  
} catch (error) {
  console.error('❌ Error:', error.message)
}
