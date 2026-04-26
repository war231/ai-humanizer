/**
 * AI Humanizer - 基础 Node.js Agent 模板
 *
 * 适用于任何 Node.js Agent 项目
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

class BasicHumanizerAgent {
    /**
     * 初始化 Agent
     * @param {string} humanizerPath - AI Humanizer 项目路径
     */
    constructor(humanizerPath = '.') {
        this.humanizerPath = humanizerPath;
        this.tempDir = require('os').tmpdir();

        // 创建临时目录
        if (!fs.existsSync(this.tempDir)) {
            fs.mkdirSync(this.tempDir, { recursive: true });
        }
    }

    /**
     * 检测文本中的 AI 写作模式
     * @param {string} text - 待检测的文本
     * @returns {Object} 检测结果
     */
    detect(text) {
        const inputFile = this._saveTempFile(text);
        const result = this._callCLI('detect', inputFile, ['--format', 'json']);
        return JSON.parse(result);
    }

    /**
     * 人性化重写文本
     * @param {string} text - 待重写的文本
     * @param {string} tone - 目标语调 (neutral/formal/casual/technical)
     * @returns {string} 重写后的文本
     */
    rewrite(text, tone = 'neutral') {
        const inputFile = this._saveTempFile(text);
        const outputFile = path.join(this.tempDir, 'output.txt');

        this._callCLI('rewrite', inputFile, ['-o', outputFile, '-t', tone]);

        return fs.readFileSync(outputFile, 'utf-8');
    }

    /**
     * 评估文本人性化程度
     * @param {string} text - 待评估的文本
     * @returns {Object} 评分结果
     */
    score(text) {
        const inputFile = this._saveTempFile(text);
        const result = this._callCLI('score', inputFile, ['--format', 'json']);
        return JSON.parse(result);
    }

    /**
     * 完整处理流程：检测 → 重写 → 评分
     * @param {string} text - 待处理的文本
     * @param {boolean} autoRewrite - 是否自动重写
     * @returns {Object} 处理结果
     */
    process(text, autoRewrite = true) {
        // Step 1: 检测
        const detection = this.detect(text);

        // Step 2: 决定是否重写
        if (autoRewrite && detection.total_patterns > 3) {
            const humanized = this.rewrite(text);
            const score = this.score(humanized);
            return {
                original: text,
                humanized: humanized,
                detection: detection,
                score: score,
                rewritten: true
            };
        } else {
            const score = this.score(text);
            return {
                original: text,
                humanized: text,
                detection: detection,
                score: score,
                rewritten: false
            };
        }
    }

    /**
     * 保存临时文件
     * @private
     */
    _saveTempFile(text) {
        const inputFile = path.join(this.tempDir, 'input.txt');
        fs.writeFileSync(inputFile, text, 'utf-8');
        return inputFile;
    }

    /**
     * 调用 CLI
     * @private
     */
    _callCLI(command, inputFile, options = []) {
        const cmd = [
            'python', '-m', 'ai_humanizer.cli',
            command, inputFile,
            ...options
        ].join(' ');

        return execSync(cmd, {
            cwd: this.humanizerPath,
            encoding: 'utf-8'
        });
    }
}

// 使用示例
if (require.main === module) {
    // 初始化 Agent
    const agent = new BasicHumanizerAgent();

    // 示例文本
    const text = `
    此外，这个项目至关重要。我们需要深入探讨其复杂性。
    这不仅仅是一个项目，而是我们思考方式的革命。
    行业专家认为这将对整个行业产生持久影响。
    `;

    // 检测
    const detection = agent.detect(text);
    console.log(`检测到 ${detection.total_patterns} 种 AI 模式`);

    // 重写
    const humanized = agent.rewrite(text);
    console.log(`重写结果: ${humanized}`);

    // 评分
    const score = agent.score(humanized);
    console.log(`质量评分: ${score.total_score}/50`);

    // 完整处理
    const result = agent.process(text);
    console.log('处理结果:', result);
}

module.exports = BasicHumanizerAgent;
