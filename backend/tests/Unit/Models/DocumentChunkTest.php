<?php

namespace Tests\Unit\Models;

use App\Models\DocumentChunk;
use App\Models\KnowledgeBase;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class DocumentChunkTest extends TestCase
{
    use RefreshDatabase;

    /** @test */
    public function it_can_create_a_document_chunk()
    {
        $knowledgeBase = KnowledgeBase::factory()->create();

        $chunk = DocumentChunk::create([
            'knowledge_base_id' => $knowledgeBase->id,
            'content' => 'This is a test chunk of text.',
            'chunk_index' => 0,
            'token_count' => 7,
            'metadata' => ['page' => 1, 'section' => 'intro'],
        ]);

        $this->assertDatabaseHas('document_chunks', [
            'id' => $chunk->id,
            'knowledge_base_id' => $knowledgeBase->id,
            'content' => 'This is a test chunk of text.',
            'chunk_index' => 0,
            'token_count' => 7,
        ]);
    }

    /** @test */
    public function it_can_retrieve_a_document_chunk()
    {
        $knowledgeBase = KnowledgeBase::factory()->create();

        $chunk = DocumentChunk::create([
            'knowledge_base_id' => $knowledgeBase->id,
            'content' => 'Test content',
            'chunk_index' => 0,
            'token_count' => 2,
        ]);

        $retrieved = DocumentChunk::find($chunk->id);

        $this->assertNotNull($retrieved);
        $this->assertEquals('Test content', $retrieved->content);
    }

    /** @test */
    public function it_belongs_to_a_knowledge_base()
    {
        $knowledgeBase = KnowledgeBase::factory()->create();

        $chunk = DocumentChunk::create([
            'knowledge_base_id' => $knowledgeBase->id,
            'content' => 'Test content',
            'chunk_index' => 0,
            'token_count' => 2,
        ]);

        $this->assertInstanceOf(KnowledgeBase::class, $chunk->knowledgeBase);
        $this->assertEquals($knowledgeBase->id, $chunk->knowledgeBase->id);
    }

    /** @test */
    public function it_casts_metadata_as_array()
    {
        $knowledgeBase = KnowledgeBase::factory()->create();

        $metadata = ['page' => 5, 'section' => 'conclusion', 'author' => 'John Doe'];

        $chunk = DocumentChunk::create([
            'knowledge_base_id' => $knowledgeBase->id,
            'content' => 'Test content',
            'chunk_index' => 0,
            'token_count' => 2,
            'metadata' => $metadata,
        ]);

        $retrieved = DocumentChunk::find($chunk->id);

        $this->assertIsArray($retrieved->metadata);
        $this->assertEquals($metadata, $retrieved->metadata);
    }

    /** @test */
    public function it_can_query_chunks_by_knowledge_base_id()
    {
        $knowledgeBase1 = KnowledgeBase::factory()->create();
        $knowledgeBase2 = KnowledgeBase::factory()->create();

        DocumentChunk::create([
            'knowledge_base_id' => $knowledgeBase1->id,
            'content' => 'Chunk 1',
            'chunk_index' => 0,
            'token_count' => 2,
        ]);

        DocumentChunk::create([
            'knowledge_base_id' => $knowledgeBase1->id,
            'content' => 'Chunk 2',
            'chunk_index' => 1,
            'token_count' => 2,
        ]);

        DocumentChunk::create([
            'knowledge_base_id' => $knowledgeBase2->id,
            'content' => 'Chunk 3',
            'chunk_index' => 0,
            'token_count' => 2,
        ]);

        $kb1Chunks = DocumentChunk::where('knowledge_base_id', $knowledgeBase1->id)->get();
        $kb2Chunks = DocumentChunk::where('knowledge_base_id', $knowledgeBase2->id)->get();

        $this->assertCount(2, $kb1Chunks);
        $this->assertCount(1, $kb2Chunks);
    }

    /** @test */
    public function it_cascade_deletes_chunks_when_knowledge_base_is_deleted()
    {
        $knowledgeBase = KnowledgeBase::factory()->create();

        $chunk = DocumentChunk::create([
            'knowledge_base_id' => $knowledgeBase->id,
            'content' => 'Test content',
            'chunk_index' => 0,
            'token_count' => 2,
        ]);

        $this->assertDatabaseHas('document_chunks', ['id' => $chunk->id]);

        $knowledgeBase->delete();

        $this->assertDatabaseMissing('document_chunks', ['id' => $chunk->id]);
    }
}
