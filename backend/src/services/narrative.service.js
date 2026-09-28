/**
 * Template-based narrative generation (Section 24: "LLM Integration").
 *
 * This module is a deterministic, dependency-free stand-in for an LLM call.
 * It builds a rich, evidence-based narrative suitable for a character certificate.
 */
function buildNarrative(assessment, evidenceCounts) {
  const top = assessment.strengths;
  const focus = assessment.developmentAreas.filter(d => assessment.scores[d] < 70);

  const strengthPhrase = top.length
    ? `has demonstrated outstanding engagement and consistent growth, particularly excelling in ${top.join(', ').replace(/_/g, ' ')}`
    : 'has built a verified and structured activity record';

  const evidenceBits = [];
  if (evidenceCounts.academic_engagement) evidenceBits.push(`${evidenceCounts.academic_engagement} academic milestones and daily classroom engagements`);
  if (evidenceCounts.learning_orientation) evidenceBits.push(`${evidenceCounts.learning_orientation} instances of deep learning, including library visits and reading sessions`);
  if (evidenceCounts.technical_engagement) evidenceBits.push(`${evidenceCounts.technical_engagement} technical projects and practical applications`);
  if (evidenceCounts.creativity) evidenceBits.push(`${evidenceCounts.creativity} creative endeavors, games, and strategy sessions`);
  if (evidenceCounts.leadership) evidenceBits.push(`${evidenceCounts.leadership} leadership roles and organizational responsibilities`);
  if (evidenceCounts.extracurricular_involvement) evidenceBits.push(`${evidenceCounts.extracurricular_involvement} extracurricular events and college participations`);
  if (evidenceCounts.community_participation) evidenceBits.push(`${evidenceCounts.community_participation} community and social service activities`);

  const evidenceSentence = evidenceBits.length
    ? ` Throughout their academic journey, the candidate's development is evidenced by ${evidenceBits.join(', ')}.`
    : '';

  const archetypeSentence = assessment.archetype 
    ? `\n\nOverall, the student embodies the profile of a "${assessment.archetype}", showcasing a holistic character built on verifiable achievements.`
    : '';

  const focusSentence = focus.length
    ? ` Moving forward, continued involvement in ${focus.join(' and ').replace(/_/g, ' ')} will further enrich their professional and personal character.`
    : ' The student maintains a highly balanced and exemplary engagement across all dimensions of character development.';

  return (
    `This certificate verifies that the student ${strengthPhrase} during their degree program.` +
    `${evidenceSentence}` +
    `${focusSentence}` +
    `${archetypeSentence}`
  );
}

module.exports = { buildNarrative };
